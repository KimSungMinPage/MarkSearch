import re
_ws = re.compile(r"\s+")
def clean_text(value: object | None) -> str:
    return _ws.sub(" ", "" if value is None else str(value).replace("\r", " ").replace("\n", " ")).strip()
