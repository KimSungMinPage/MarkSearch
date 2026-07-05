import json
from typing import Any
from app.constants import SETTINGS_PATH
DEFAULT_SETTINGS: dict[str, Any] = {"geometry":"1200x760","selected_tab":0,"last_save_dir":"","num_of_rows":100,"key_mode":"자동 감지","remember_key":False}
class SettingsService:
    def load(self) -> dict[str, Any]:
        try:
            if SETTINGS_PATH.exists(): return {**DEFAULT_SETTINGS, **json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))}
        except Exception: pass
        return DEFAULT_SETTINGS.copy()
    def save(self, settings: dict[str, Any]) -> None:
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        safe = {k:v for k,v in settings.items() if k != "service_key"}
        SETTINGS_PATH.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
