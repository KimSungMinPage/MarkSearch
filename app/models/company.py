from dataclasses import dataclass
@dataclass
class Company:
    induty: str = ""; entrps: str = ""; normalized_entrps: str = ""; rprsntv: str = ""; prmisn_dt: str = ""; prmisn_date_display: str = ""; is_valid_date: bool = False; adres: str = ""; prmisn_no: str = ""; sido: str = ""; sigungu: str = ""; selected: bool = False; is_duplicate: bool = False; duplicate_group_no: int = 0
    def duplicate_key(self) -> tuple[str, str, str, str]: return (self.prmisn_no, self.induty, self.entrps, self.adres)
