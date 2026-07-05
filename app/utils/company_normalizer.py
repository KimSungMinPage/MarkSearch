import re
from .text_utils import clean_text
_PAT = re.compile(r"주식회사|㈜|\(주\)|（주）")
def normalize_company_name(name: str | None) -> str:
    return clean_text(_PAT.sub("", clean_text(name)))
