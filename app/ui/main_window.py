import queue, threading, tkinter as tk
from tkinter import ttk
from app.constants import APP_TITLE
from app.models import Company, Factory
from app.services.api_client import DataGoApiClient
from app.services.credential_service import CredentialService
from app.services.logging_service import LoggingService
from app.services.settings_service import SettingsService
from app.ui.api_settings_tab import ApiSettingsTab
from app.ui.collection_tab import CollectionTab
from app.ui.results_tab import ResultsTab
from app.ui.statistics_tab import StatisticsTab
from app.ui.logs_tab import LogsTab
class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__(); self.title(APP_TITLE); self.geometry("1200x760"); self.minsize(1000,650)
        self.queue: queue.Queue = queue.Queue(); self.cancel_event=threading.Event(); self.companies:list[Company]=[]; self.factories:list[Factory]=[]
        self.settings_service=SettingsService(); self.credential_service=CredentialService(); self.logger=LoggingService(); self.api=DataGoApiClient()
        self.notebook=ttk.Notebook(self); self.notebook.pack(fill="both", expand=True)
        self.api_tab=ApiSettingsTab(self.notebook,self); self.collection_tab=CollectionTab(self.notebook,self); self.results_tab=ResultsTab(self.notebook,self); self.statistics_tab=StatisticsTab(self.notebook,self); self.logs_tab=LogsTab(self.notebook,self)
        for title,tab in [("API 설정",self.api_tab),("데이터 수집",self.collection_tab),("수집 결과",self.results_tab),("통계",self.statistics_tab),("로그",self.logs_tab)]: self.notebook.add(tab,text=title)
        self.after(100,self._process_queue)
    def refresh_all(self) -> None:
        self.results_tab.refresh(); self.statistics_tab.refresh(); self.logs_tab.refresh()
    def _process_queue(self) -> None:
        while not self.queue.empty():
            kind,payload=self.queue.get()
            if kind=="progress": self.collection_tab.update_progress(payload)
            elif kind=="done": self.refresh_all(); self.collection_tab.set_running(False)
            elif kind=="log": self.logs_tab.refresh()
        self.after(100,self._process_queue)
