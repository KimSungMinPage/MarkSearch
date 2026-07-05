from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.services.excel_export_service import ExcelExportService
from app.services.csv_export_service import CsvExportService
from app.utils.date_utils import timestamp_for_filename
class ResultsTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=8); self.app=app; toolbar=ttk.Frame(self); toolbar.pack(fill="x"); self.search=tk.StringVar(); ttk.Entry(toolbar,textvariable=self.search,width=30).pack(side="left"); ttk.Button(toolbar,text="검색",command=self.refresh).pack(side="left"); ttk.Button(toolbar,text="전체 선택",command=lambda:self._select(True)).pack(side="left"); ttk.Button(toolbar,text="선택 해제",command=lambda:self._select(False)).pack(side="left"); ttk.Button(toolbar,text="Excel 저장",command=self.export_excel).pack(side="left"); ttk.Button(toolbar,text="CSV 저장",command=self.export_csv).pack(side="left")
        nb=ttk.Notebook(self); nb.pack(fill="both",expand=True); self.company_tree=self._tree(nb,["선택","업종","업체명","대표자명","업체허가일자","업체허가번호","공장주소","시도","시군구","중복"]); self.factory_tree=self._tree(nb,["선택","업체명","업종","업체허가번호","대표자명","업체허가일자","공장일련번호","공장명","공장전화번호","공장주소1","공장주소2","통합공장주소","시도","시군구","중복"]); nb.add(self.company_tree.master,text="업체 목록"); nb.add(self.factory_tree.master,text="제조소 상세")
    def _tree(self,parent,cols):
        frame=ttk.Frame(parent); tree=ttk.Treeview(frame,columns=cols,show="headings",height=22); vs=ttk.Scrollbar(frame,orient="vertical",command=tree.yview); hs=ttk.Scrollbar(frame,orient="horizontal",command=tree.xview); tree.configure(yscrollcommand=vs.set,xscrollcommand=hs.set)
        for c in cols: tree.heading(c,text=c); tree.column(c,width=120,anchor="w")
        tree.grid(row=0,column=0,sticky="nsew"); vs.grid(row=0,column=1,sticky="ns"); hs.grid(row=1,column=0,sticky="ew"); frame.rowconfigure(0,weight=1); frame.columnconfigure(0,weight=1); return tree
    def refresh(self):
        q=self.search.get().strip(); self.company_tree.delete(*self.company_tree.get_children()); self.factory_tree.delete(*self.factory_tree.get_children())
        for r in self.app.companies[:5000]:
            if q and q not in r.entrps: continue
            self.company_tree.insert("", "end", values=["Y" if r.selected else "",r.induty,r.entrps,r.rprsntv,r.prmisn_date_display,r.prmisn_no,r.adres,r.sido,r.sigungu,"Y" if r.is_duplicate else "N"])
        for r in self.app.factories[:5000]:
            if q and q not in r.entrps: continue
            self.factory_tree.insert("", "end", values=["Y" if r.selected else "",r.entrps,r.induty,r.prmisn_no,r.rprsntv,r.prmisn_date_display,r.sn,r.fctry_nm,r.telno,r.fctry_addr1,r.fctry_addr2,r.combined_address,r.sido,r.sigungu,"Y" if r.is_duplicate else "N"])
    def _select(self,value):
        for r in self.app.companies+self.app.factories: r.selected=value
        self.refresh()
    def export_excel(self):
        path=filedialog.asksaveasfilename(defaultextension=".xlsx",initialfile=f"의약품_업체허가현황_{timestamp_for_filename()}.xlsx",filetypes=[("Excel","*.xlsx")])
        if path: ExcelExportService().export(path,self.app.companies,self.app.factories); messagebox.showinfo("완료",f"저장했습니다.\n{path}")
    def export_csv(self):
        folder=filedialog.askdirectory()
        if folder:
            svc=CsvExportService(); svc.export_companies(Path(folder)/f"의약품_업체목록_{timestamp_for_filename()}.csv",self.app.companies); svc.export_factories(Path(folder)/f"의약품_제조소상세_{timestamp_for_filename()}.csv",self.app.factories); messagebox.showinfo("완료","CSV 저장이 완료되었습니다.")
