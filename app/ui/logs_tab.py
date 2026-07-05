import os
from tkinter import ttk
from app.constants import LOG_DIR
class LogsTab(ttk.Frame):
    def __init__(self,parent,app): super().__init__(parent,padding=8); self.app=app; bar=ttk.Frame(self); bar.pack(fill="x"); ttk.Button(bar,text="로그 지우기",command=self.clear).pack(side="left"); ttk.Button(bar,text="로그 폴더 열기",command=self.open_folder).pack(side="left"); self.list=ttk.Treeview(self,columns=["로그"],show="headings"); self.list.heading("로그",text="로그"); self.list.pack(fill="both",expand=True)
    def refresh(self): self.list.delete(*self.list.get_children()); [self.list.insert("","end",values=[e]) for e in self.app.logger.entries[-1000:]]
    def clear(self): self.app.logger.entries.clear(); self.refresh()
    def open_folder(self): LOG_DIR.mkdir(parents=True,exist_ok=True); os.startfile(LOG_DIR) if hasattr(os,"startfile") else None
