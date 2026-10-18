SESSION_LIMIT = 5
WINDOW_SECONDS = 600
DAILY_LIMIT = 40
DAY_SECONDS = 86400


def allow_request(history, now, limit, window):
    """Return True if fewer than `limit` requests happened in the last `window` seconds."""
    recent = [t for t in history if now - t < window]
    return len(recent) < limit