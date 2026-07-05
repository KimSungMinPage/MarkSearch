import time, threading, tkinter as tk
from tkinter import ttk, messagebox
from app.models import CollectionOptions, KeyMode
class ApiSettingsTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=16); self.app=app; self.key_var=tk.StringVar(value=app.credential_service.load_key()); self.mode_var=tk.StringVar(value=KeyMode.AUTO.value); self.remember_var=tk.BooleanVar(value=False); self.result_var=tk.StringVar(value="서비스키를 입력하고 API 연결 테스트를 실행하십시오.")
        ttk.Label(self,text="서비스키").grid(row=0,column=0,sticky="w"); self.entry=ttk.Entry(self,textvariable=self.key_var,show="*",width=90); self.entry.grid(row=0,column=1,sticky="ew")
        ttk.Button(self,text="보이기/숨기기",command=self.toggle).grid(row=0,column=2); ttk.Checkbutton(self,text="인증키 기억하기",variable=self.remember_var).grid(row=1,column=1,sticky="w")
        ttk.Combobox(self,textvariable=self.mode_var,values=[m.value for m in KeyMode],state="readonly").grid(row=2,column=1,sticky="w")
        ttk.Button(self,text="API 연결 테스트",command=self.test).grid(row=3,column=1,sticky="w"); ttk.Button(self,text="저장된 키 삭제",command=self.delete_key).grid(row=3,column=2)
        ttk.Label(self,textvariable=self.result_var,wraplength=900).grid(row=4,column=0,columnspan=3,sticky="w",pady=12); self.columnconfigure(1,weight=1)
    def toggle(self): self.entry.configure(show="" if self.entry.cget("show") else "*")
    def options(self): return CollectionOptions(service_key=self.key_var.get(), key_mode=KeyMode(self.mode_var.get()), num_of_rows=1)
    def test(self): threading.Thread(target=self._test_worker,daemon=True).start()
    def _test_worker(self):
        try:
            start=time.time(); res=self.app.api.get_company_page(self.options(),1); elapsed=time.time()-start
            msg=f"API 연결에 성공했습니다. 전체 검색 결과: {res.body.total_count:,}건 응답 시간: {elapsed:.2f}초" if res.is_success else res.header.result_msg
            if self.remember_var.get() and not self.app.credential_service.save_key(self.key_var.get()): msg += "\n서비스키를 안전하게 저장하지 못했습니다. 이번 실행 중에는 사용할 수 있지만 프로그램 종료 후에는 저장되지 않습니다."
            self.result_var.set(msg); self.app.logger.info("API 연결 테스트 완료")
        except Exception as e: self.result_var.set(f"API 연결에 실패했습니다. 서비스키와 네트워크를 확인하십시오. {e}"); self.app.logger.error(str(e))
    def delete_key(self): self.app.credential_service.delete_key(); self.key_var.set(""); messagebox.showinfo("완료","저장된 인증키를 삭제했습니다.")
