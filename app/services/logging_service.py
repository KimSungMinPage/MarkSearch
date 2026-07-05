import logging
from datetime import datetime
from app.constants import LOG_DIR
from app.utils.sensitive_data_masker import mask_url
class LoggingService:
    def __init__(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True); self.entries: list[str] = []
        self.logger = logging.getLogger("GmpCompanyCollector"); self.logger.setLevel(logging.INFO); self.logger.handlers.clear()
        handler = logging.FileHandler(LOG_DIR / f"GmpCompanyCollector_{datetime.now():%Y%m%d}.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")); self.logger.addHandler(handler)
    def log(self, level: str, message: str) -> None:
        safe = mask_url(message); line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {level}: {safe}"; self.entries.append(line)
        getattr(self.logger, {"정보":"info","경고":"warning","오류":"error"}.get(level,"info"))(safe)
    def info(self, m: str) -> None: self.log("정보", m)
    def warning(self, m: str) -> None: self.log("경고", m)
    def error(self, m: str) -> None: self.log("오류", m)
