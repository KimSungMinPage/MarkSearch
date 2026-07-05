from zipfile import ZipFile
from app.models import Company, Factory
from app.services.excel_export_service import ExcelExportService
from app.services.csv_export_service import CsvExportService
def test_excel_and_csv(tmp_path):
    x=tmp_path/'out.xlsx'; c=Company(entrps='한글', prmisn_no='0123'); f=Factory(entrps='한글', telno='010', prmisn_no='0001')
    ExcelExportService().export(x,[c],[f]); assert x.exists()
    with ZipFile(x) as z:
        names=z.namelist(); content='\n'.join(z.read(n).decode('utf-8', errors='ignore') for n in names if n.endswith('.xml'))
        assert '업체목록' in content and '제조소상세' in content and '0123' in content and '010' in content and '한글' in content
    csv_path=tmp_path/'c.csv'; CsvExportService().export_companies(csv_path,[c]); assert csv_path.read_bytes().startswith(b'\xef\xbb\xbf') and '한글' in csv_path.read_text(encoding='utf-8-sig')
