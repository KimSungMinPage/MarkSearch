from dataclasses import dataclass
@dataclass
class Factory:
    entrps: str = ""; normalized_entrps: str = ""; induty: str = ""; prmisn_no: str = ""; rprsntv: str = ""; prmisn_dt: str = ""; prmisn_date_display: str = ""; is_valid_date: bool = False; sn: str = ""; fctry_nm: str = ""; telno: str = ""; fctry_addr1: str = ""; fctry_addr2: str = ""; combined_address: str = ""; sido: str = ""; sigungu: str = ""; selected: bool = False; is_duplicate: bool = False; duplicate_group_no: int = 0
    def duplicate_key(self) -> tuple[str, str, str, str, str]: return (self.prmisn_no, self.sn, self.fctry_nm, self.fctry_addr1, self.fctry_addr2)
