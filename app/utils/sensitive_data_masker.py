import re
def mask_key(key: str | None) -> str:
    key = (key or "").strip()
    return "****" if len(key) <= 8 else f"{key[:4]}****{key[-4:]}"
def mask_url(url: str) -> str:
    return re.sub(r"serviceKey=[^&\s]+", "serviceKey=***", url, flags=re.I)
