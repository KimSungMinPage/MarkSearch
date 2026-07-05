import threading, tkinter as tk
from tkinter import ttk
from app.constants import PAGE_SIZE_OPTIONS
from app.models import CollectionOptions, CollectionKind, KeyMode
from app.services.collection_service import collect_pages
from app.utils.duplicate_detector import mark_duplicates
class CollectionTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=16); self.app=app; self.kind=tk.StringVar(value=CollectionKind.BOTH.value); self.induty=tk.StringVar(); self.entrps=tk.StringVar(); self.dt=tk.StringVar(); self.no=tk.StringVar(); self.rows=tk.IntVar(value=100); self.progress=tk.StringVar(value="대기 중")
        for i,(label,var) in enumerate([("수집 종류",self.kind),("업종",self.induty),("업체명",self.entrps),("업체허가일자",self.dt),("업체허가번호",self.no)]): ttk.Label(self,text=label).grid(row=i,column=0,sticky="w"); (ttk.Combobox(self,textvariable=var,values=[k.value for k in CollectionKind],state="readonly") if i==0 else ttk.Entry(self,textvariable=var)).grid(row=i,column=1,sticky="ew")
        ttk.Label(self,text="페이지당 건수").grid(row=5,column=0); ttk.Combobox(self,textvariable=self.rows,values=PAGE_SIZE_OPTIONS,state="readonly").grid(row=5,column=1,sticky="w")
        self.start_btn=ttk.Button(self,text="수집 시작",command=self.start); self.start_btn.grid(row=6,column=1,sticky="w"); self.cancel_btn=ttk.Button(self,text="수집 취소",command=self.cancel,state="disabled"); self.cancel_btn.grid(row=6,column=1); ttk.Button(self,text="결과 초기화",command=self.clear).grid(row=6,column=1,sticky="e")
        ttk.Label(self,textvariable=self.progress).grid(row=7,column=0,columnspan=2,sticky="w",pady=8); self.bar=ttk.Progressbar(self,maximum=100); self.bar.grid(row=8,column=0,columnspan=2,sticky="ew"); self.columnconfigure(1,weight=1)
    def _options(self):
        return CollectionOptions(self.app.api_tab.key_var.get(), KeyMode(self.app.api_tab.mode_var.get()), CollectionKind(self.kind.get()), self.induty.get(), self.entrps.get(), self.dt.get(), self.no.get(), int(self.rows.get()))
    def start(self): self.set_running(True); self.app.cancel_event.clear(); threading.Thread(target=self._worker,daemon=True).start()
    def _worker(self):
        opts=self._options()
        try:
            if opts.kind != CollectionKind.FACTORIES: self.app.companies=collect_pages(lambda p:self.app.api.get_company_page(opts,p),opts.num_of_rows,self.app.cancel_event,lambda x:self.app.queue.put(("progress",x)))
            if opts.kind != CollectionKind.COMPANIES: self.app.factories=collect_pages(lambda p:self.app.api.get_factory_page(opts,p),opts.num_of_rows,self.app.cancel_event,lambda x:self.app.queue.put(("progress",x)))
            mark_duplicates(self.app.companies); mark_duplicates(self.app.factories); self.app.logger.info("데이터 수집 완료")
        except Exception as e: self.app.logger.error(str(e)); self.progress.set(f"오류: {e}")
        self.app.queue.put(("done",None))
    def cancel(self): self.app.cancel_event.set(); self.progress.set("취소 요청됨")
    def clear(self): self.app.companies.clear(); self.app.factories.clear(); self.app.refresh_all(); self.progress.set("결과 초기화 완료")
    def set_running(self, running: bool): self.start_btn.configure(state="disabled" if running else "normal"); self.cancel_btn.configure(state="normal" if running else "disabled")
    def update_progress(self,p): self.progress.set(f"현재 {p['current_page']} / {p['total_pages']}페이지, 수집 {p['received_count']} / {p['total_count']}건, 경과 {p['elapsed']:.1f}초"); self.bar['value']=p['percent']
