# helpers/get_create.py — stub
def get_creation_date(user_id: int) -> str:
    """Approximate account creation date from user_id."""
    import datetime
    # Rough estimate: Telegram started assigning IDs around 2013
    # This is a best-effort approximation
    try:
        epoch = 1356998400  # Jan 1 2013
        step = 1000
        approx_ts = epoch + (user_id // step)
        dt = datetime.datetime.utcfromtimestamp(approx_ts)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"
