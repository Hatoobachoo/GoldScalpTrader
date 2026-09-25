"""Correlation helpers for setup evidence."""
def unique_source_fraction(source_ids: tuple[str,...])->float:
    return 0.0 if not source_ids else len(set(source_ids))/len(source_ids)
