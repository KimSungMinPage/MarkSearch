import csv
from pathlib import Path
from app.models import Company, Factory
class CsvExportService:
    def export_companies(self, path: str | Path, rows: list[Company]) -> None:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w=csv.writer(f); w.writerow(["번호","업종","업체명","대표자명","업체허가일자","업체허가번호","공장주소","시도","시군구","중복여부"])
            for i,r in enumerate(rows,1): w.writerow([i,r.induty,r.entrps,r.rprsntv,r.prmisn_date_display,r.prmisn_no,r.adres,r.sido,r.sigungu,"Y" if r.is_duplicate else "N"])
    def export_factories(self, path: str | Path, rows: list[Factory]) -> None:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w=csv.writer(f); w.writerow(["번호","업체명","업종","업체허가번호","대표자명","업체허가일자","공장일련번호","공장명","공장전화번호","공장주소1","공장주소2","통합공장주소","시도","시군구","중복여부"])
            for i,r in enumerate(rows,1): w.writerow([i,r.entrps,r.induty,r.prmisn_no,r.rprsntv,r.prmisn_date_display,r.sn,r.fctry_nm,r.telno,r.fctry_addr1,r.fctry_addr2,r.combined_address,r.sido,r.sigungu,"Y" if r.is_duplicate else "N"])
