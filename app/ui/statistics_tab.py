from tkinter import ttk
from app.services.statistics_service import StatisticsService
class StatisticsTab(ttk.Frame):
    def __init__(self,parent,app): super().__init__(parent,padding=16); self.app=app; self.text=ttk.Label(self,text="수집 후 통계가 표시됩니다.",justify="left"); self.text.pack(anchor="w")
    def refresh(self):
        b=StatisticsService().basic(self.app.companies,self.app.factories); self.text.configure(text=f"전체 업체 레코드 수: {b.company_records}\n고유 업체 수: {b.unique_companies}\n고유 허가번호 수: {b.unique_permits}\n전체 제조소 수: {b.factories}\n주소 보유 제조소 수: {b.factories_with_address}\n전화번호 보유 제조소 수: {b.factories_with_phone}\n필수정보 누락 건수: {b.missing_company_name+b.missing_permit_no+b.missing_address}\n중복 의심 건수: {b.duplicates}")
