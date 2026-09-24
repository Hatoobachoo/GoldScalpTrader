# GoldScalpTrader

Safety-first local MetaTrader 5 gold scalping project.

## Non-negotiable project rules

- Trading runs locally on the user's Windows PC and MetaTrader 5 terminal.
- GitHub is used only for source control and backup.
- GitHub Actions, Codespaces, Git LFS, paid Marketplace services, and paid external APIs are not required.
- `DRY_RUN` is the default operating mode.
- Live order execution must never be enabled accidentally.
- Credentials, account numbers, passwords, tokens, and `.env` files must never be committed.
- One-position-at-a-time and hard risk controls are part of the design.
- No martingale, unlimited averaging, or uncontrolled grid logic.

> Important: automated trading can lose money. Test in dry-run/demo mode before considering live execution.

Project foundation is being built in small, reviewable milestones.