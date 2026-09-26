"""Single normalized read-only MetaTrader 5 boundary.

Only this module imports/owns MetaTrader5 analytical and recovery reads.
Irreversible broker operations are intentionally absent and belong exclusively
to ``execution/mt5_writer.py``.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import DataQuality, Direction, Timeframe
from gold_scalp_trader.domain.market import AccountFacts, Candle, MarketSnapshot, PositionFacts, Quote, SymbolSpec
from gold_scalp_trader.market_data.activity import DealFacts
from .snapshot import build_snapshot

UTC = timezone.utc


class Mt5Like(Protocol):
    def account_info(self) -> Any: ...
    def symbol_info(self, symbol: str) -> Any: ...
    def symbol_info_tick(self, symbol: str) -> Any: ...
    def copy_rates_from_pos(self, symbol: str, timeframe: int, start_pos: int, count: int) -> Any: ...
    def positions_get(self, symbol: str | None = None) -> Any: ...
    def history_deals_get(self, date_from: datetime, date_to: datetime, *, position: int | None = None) -> Any: ...


@dataclass(frozen=True, slots=True)
class ReadResult:
    snapshot: MarketSnapshot
    resolved_symbol: str


class Mt5ReadError(RuntimeError):
    pass


def _field(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError):
        pass
    try:
        return obj[name]
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def _utc_from_epoch(seconds: int | float) -> datetime:
    return datetime.fromtimestamp(float(seconds), tz=UTC)


def _load_mt5() -> Any:
    try:
        import MetaTrader5 as mt5  # type: ignore
    except ImportError as exc:
        raise Mt5ReadError("MetaTrader5 package is not installed") from exc
    return mt5


def _deal_entry_role(api: Any, value: Any) -> str:
    mapping = {
        getattr(api, "DEAL_ENTRY_IN", 0): "IN",
        getattr(api, "DEAL_ENTRY_OUT", 1): "OUT",
        getattr(api, "DEAL_ENTRY_INOUT", 2): "INOUT",
        getattr(api, "DEAL_ENTRY_OUT_BY", 3): "OUT_BY",
    }
    return mapping.get(value, f"UNKNOWN:{value}")


def _deal_type(api: Any, value: Any) -> tuple[str, Direction | None]:
    buy = getattr(api, "DEAL_TYPE_BUY", 0)
    sell = getattr(api, "DEAL_TYPE_SELL", 1)
    if value == buy:
        return "BUY", Direction.BUY
    if value == sell:
        return "SELL", Direction.SELL
    labels = {
        getattr(api, "DEAL_TYPE_BALANCE", 2): "BALANCE",
        getattr(api, "DEAL_TYPE_CREDIT", 3): "CREDIT",
        getattr(api, "DEAL_TYPE_CHARGE", 4): "DEBIT",
        getattr(api, "DEAL_TYPE_CORRECTION", 5): "CORRECTION",
        getattr(api, "DEAL_TYPE_BONUS", 6): "BONUS",
        getattr(api, "DEAL_TYPE_COMMISSION", 7): "COMMISSION",
        getattr(api, "DEAL_TYPE_COMMISSION_DAILY", 8): "COMMISSION",
        getattr(api, "DEAL_TYPE_COMMISSION_MONTHLY", 9): "COMMISSION",
        getattr(api, "DEAL_TYPE_AGENT_DAILY", 10): "AGENT",
        getattr(api, "DEAL_TYPE_AGENT_MONTHLY", 11): "AGENT",
        getattr(api, "DEAL_TYPE_INTEREST", 12): "INTEREST",
        getattr(api, "DEAL_TYPE_BUY_CANCELED", 13): "BUY_CANCELED",
        getattr(api, "DEAL_TYPE_SELL_CANCELED", 14): "SELL_CANCELED",
        getattr(api, "DEAL_DIVIDEND", 15): "DIVIDEND",
        getattr(api, "DEAL_DIVIDEND_FRANKED", 16): "DIVIDEND",
        getattr(api, "DEAL_TAX", 17): "TAX",
    }
    return labels.get(value, f"UNKNOWN:{value}"), None


def _normalize_deals(api: Any, raw: Any, *, position_filter: int | None = None) -> tuple[DealFacts, ...]:
    deals: list[DealFacts] = []
    try:
        for item in raw:
            position_id_raw = _field(item, "position_id", None)
            position_id = None if position_id_raw in (None, 0) else int(position_id_raw)
            if position_filter is not None and position_id not in {None, position_filter}:
                continue
            deal_type, direction = _deal_type(api, _field(item, "type", None))
            source_msc = _field(item, "time_msc", None)
            time_utc = (
                datetime.fromtimestamp(float(source_msc) / 1000.0, tz=UTC)
                if source_msc not in (None, 0)
                else _utc_from_epoch(_field(item, "time"))
            )
            deals.append(
                DealFacts(
                    ticket=int(_field(item, "ticket")),
                    position_id=position_id,
                    symbol=str(_field(item, "symbol", "") or ""),
                    direction=direction,
                    volume=float(_field(item, "volume", 0.0) or 0.0),
                    profit=float(_field(item, "profit", 0.0) or 0.0),
                    commission=float(_field(item, "commission", 0.0) or 0.0),
                    swap=float(_field(item, "swap", 0.0) or 0.0),
                    fee=float(_field(item, "fee", 0.0) or 0.0),
                    magic=_optional_int(_field(item, "magic", None)),
                    entry_role=_deal_entry_role(api, _field(item, "entry", None)),
                    deal_type=deal_type,
                    time_utc=time_utc,
                    comment=str(_field(item, "comment", "") or ""),
                )
            )
    except (TypeError, ValueError) as exc:
        raise Mt5ReadError("deal history is corrupt/incomplete") from exc
    return tuple(sorted(deals, key=lambda deal: (deal.time_utc, deal.ticket)))


class Mt5Reader:
    def __init__(self, settings: Settings, api: Mt5Like | None = None) -> None:
        self.settings = settings
        self.api = api if api is not None else _load_mt5()

    def resolve_symbol(self) -> str:
        for symbol in self.settings.symbol_aliases:
            if self.api.symbol_info(symbol) is not None:
                return symbol
        raise Mt5ReadError(f"none of the configured Gold symbols exist: {self.settings.symbol_aliases}")

    def read(self, *, captured_at: datetime | None = None) -> ReadResult:
        captured = captured_at or datetime.now(tz=UTC)
        if captured.tzinfo is None:
            raise ValueError("captured_at must be timezone-aware")
        symbol = self.resolve_symbol()
        account = self._read_account()
        spec = self._read_symbol_spec(symbol)
        quote = self._read_quote(symbol, captured)
        candles, quality = self._read_candles(symbol, captured)
        positions, positions_quality = self._read_positions(symbol)
        snapshot = build_snapshot(
            captured_at=captured,
            account=account,
            symbol_spec=spec,
            quote=quote,
            candles=candles,
            quality=quality,
            positions=positions,
            positions_quality=positions_quality,
        )
        return ReadResult(snapshot=snapshot, resolved_symbol=symbol)

    def read_deals(self, *, from_time: datetime, to_time: datetime) -> tuple[DealFacts, ...] | None:
        """Read account-wide normalized deals for accounting/recovery."""
        if from_time.tzinfo is None or to_time.tzinfo is None:
            raise ValueError("deal-history times must be timezone-aware")
        if to_time < from_time:
            raise ValueError("to_time cannot precede from_time")
        fn = getattr(self.api, "history_deals_get", None)
        if fn is None:
            return None
        try:
            raw = fn(from_time, to_time)
        except Exception:
            return None
        if raw is None:
            return None
        return _normalize_deals(self.api, raw)

    def read_position_deals(self, position_ticket: int, *, from_time: datetime, to_time: datetime) -> tuple[DealFacts, ...] | None:
        if position_ticket <= 0:
            raise ValueError("position_ticket must be positive")
        if from_time.tzinfo is None or to_time.tzinfo is None:
            raise ValueError("deal-history times must be timezone-aware")
        if to_time < from_time:
            raise ValueError("to_time cannot precede from_time")
        fn = getattr(self.api, "history_deals_get", None)
        if fn is None:
            return None
        try:
            raw = fn(from_time, to_time, position=position_ticket)
        except Exception:
            return None
        if raw is None:
            return None
        return _normalize_deals(self.api, raw, position_filter=position_ticket)

    def account_positions_clear(self) -> bool | None:
        """Return whole-account flatness without conflating read failure with zero."""
        fn = getattr(self.api, "positions_get", None)
        if fn is None:
            return None
        try:
            raw = fn()
        except Exception:
            return None
        if raw is None:
            return None
        try:
            return len(raw) == 0
        except TypeError:
            return None

    def _read_account(self) -> AccountFacts:
        raw = self.api.account_info()
        if raw is None:
            raise Mt5ReadError("account_info unavailable")
        try:
            return AccountFacts(
                int(_field(raw, "login")), str(_field(raw, "server")), str(_field(raw, "currency")),
                float(_field(raw, "balance")), float(_field(raw, "equity")), float(_field(raw, "margin_free")),
                _optional_bool(_field(raw, "trade_allowed")), _optional_bool(_field(raw, "trade_expert")),
            )
        except (TypeError, ValueError) as exc:
            raise Mt5ReadError("account_info is corrupt/incomplete") from exc

    def _read_symbol_spec(self, symbol: str) -> SymbolSpec:
        raw = self.api.symbol_info(symbol)
        if raw is None:
            raise Mt5ReadError("symbol_info unavailable")
        tick_value = _field(raw, "trade_tick_value", None)
        try:
            return SymbolSpec(
                symbol=symbol, digits=int(_field(raw, "digits")), point=float(_field(raw, "point")),
                tick_size=float(_field(raw, "trade_tick_size", _field(raw, "point"))),
                tick_value=None if tick_value in (None, 0) else float(tick_value),
                volume_min=float(_field(raw, "volume_min")), volume_max=float(_field(raw, "volume_max")),
                volume_step=float(_field(raw, "volume_step")), stops_level_points=int(_field(raw, "trade_stops_level", 0) or 0),
                freeze_level_points=int(_field(raw, "trade_freeze_level", 0) or 0), trade_mode=_field(raw, "trade_mode", None),
                filling_mode=_field(raw, "filling_mode", None),
            )
        except (TypeError, ValueError) as exc:
            raise Mt5ReadError("symbol_info is corrupt/incomplete") from exc

    def _read_quote(self, symbol: str, captured: datetime) -> Quote:
        raw = self.api.symbol_info_tick(symbol)
        if raw is None:
            raise Mt5ReadError("symbol quote unavailable")
        source_msc = _field(raw, "time_msc", None)
        source_time = datetime.fromtimestamp(float(source_msc) / 1000.0, tz=UTC) if source_msc is not None else _utc_from_epoch(_field(raw, "time"))
        try:
            quote = Quote(float(_field(raw, "bid")), float(_field(raw, "ask")), source_time, captured)
        except (TypeError, ValueError) as exc:
            raise Mt5ReadError("quote is corrupt/incomplete") from exc
        if quote.age_seconds < -2.0:
            raise Mt5ReadError("quote timestamp is materially in the future")
        return quote

    def _read_candles(self, symbol: str, captured: datetime) -> tuple[dict[Timeframe, tuple[Candle, ...]], dict[Timeframe, DataQuality]]:
        counts = {Timeframe.M1:self.settings.m1_history_bars,Timeframe.M5:self.settings.m5_history_bars,Timeframe.M15:self.settings.m15_history_bars,Timeframe.H1:self.settings.h1_history_bars,Timeframe.H4:self.settings.h4_history_bars}
        output: dict[Timeframe, tuple[Candle, ...]] = {}; quality: dict[Timeframe, DataQuality] = {}
        for timeframe,count in counts.items():
            raw=self.api.copy_rates_from_pos(symbol,self._timeframe_constant(timeframe),1,count)
            if raw is None:
                output[timeframe]=(); quality[timeframe]=DataQuality.UNKNOWN; continue
            candles=[]
            try:
                for row in raw:
                    candle=Candle(timeframe,_utc_from_epoch(_field(row,"time")),float(_field(row,"open")),float(_field(row,"high")),float(_field(row,"low")),float(_field(row,"close")),int(_field(row,"tick_volume",0) or 0),int(_field(row,"real_volume",0) or 0))
                    if candle.close_time<=captured:candles.append(candle)
                candles.sort(key=lambda candle:candle.open_time)
                if any(a.open_time==b.open_time for a,b in zip(candles,candles[1:])):raise ValueError("duplicate candle timestamp")
            except (TypeError,ValueError) as exc:raise Mt5ReadError(f"{timeframe.value} candle data corrupt") from exc
            output[timeframe]=tuple(candles); quality[timeframe]=DataQuality.HEALTHY if len(candles)>=min(count,50) else DataQuality.INSUFFICIENT
        return output,quality

    def _timeframe_constant(self,timeframe:Timeframe)->int:
        value=getattr(self.api,f"TIMEFRAME_{timeframe.value}",None)
        if value is not None:return int(value)
        return {Timeframe.M1:1,Timeframe.M5:5,Timeframe.M15:15,Timeframe.H1:60,Timeframe.H4:240}[timeframe]

    def _read_positions(self,symbol:str)->tuple[tuple[PositionFacts,...]|None,DataQuality]:
        raw=self.api.positions_get(symbol=symbol)
        if raw is None:return None,DataQuality.UNKNOWN
        result=[]
        for item in raw:
            type_value=int(_field(item,"type",-1)); direction=Direction.BUY if type_value==0 else Direction.SELL if type_value==1 else Direction.NONE
            if direction is Direction.NONE:raise Mt5ReadError("position direction is unknown")
            sl=float(_field(item,"sl",0.0) or 0.0); tp=float(_field(item,"tp",0.0) or 0.0)
            result.append(PositionFacts(int(_field(item,"ticket")),str(_field(item,"symbol")),direction,float(_field(item,"volume")),float(_field(item,"price_open")),None if sl==0.0 else sl,None if tp==0.0 else tp,_optional_int(_field(item,"magic",None)),str(_field(item,"comment","") or "")))
        return tuple(result),DataQuality.HEALTHY


def _optional_bool(value: Any) -> bool | None:
    return None if value is None else bool(value)


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)
