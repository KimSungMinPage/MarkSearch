from .text_utils import clean_text
SIDOS = ["서울특별시","부산광역시","대구광역시","인천광역시","광주광역시","대전광역시","울산광역시","세종특별자치시","경기도","강원특별자치도","강원도","충청북도","충청남도","전북특별자치도","전라북도","전라남도","경상북도","경상남도","제주특별자치도"]
def combine_factory_address(addr1: str | None, addr2: str | None) -> str:
    return " ".join(x for x in (clean_text(addr1), clean_text(addr2)) if x)
def parse_address(address: str | None) -> tuple[str, str]:
    text = clean_text(address)
    if not text: return "", ""
    parts = text.split()
    sido = next((s for s in SIDOS if text.startswith(s)), parts[0] if parts else "")
    sigungu = next((p for p in parts[1:] if p.endswith(("시","군","구"))), "")
    return sido, sigungu
