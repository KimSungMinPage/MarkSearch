from datetime import datetime
from .text_utils import clean_text
def parse_prmisn_date(raw: str | None) -> tuple[str, bool]:
    value = clean_text(raw)
    if len(value) == 8 and value.isdigit():
        try: return datetime.strptime(value, "%Y%m%d").strftime("%Y-%m-%d"), True
        except ValueError: pass
    return value, False
def timestamp_for_filename() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
