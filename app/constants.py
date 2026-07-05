from pathlib import Path
import os
APP_NAME = "GmpCompanyCollector"
APP_TITLE = "GMP 업체·제조소 데이터 수집기"
BASE_URL = "http://apis.data.go.kr/1471000/DrugEtcBsshBspmStusService"
LIST_ENDPOINT = "getDrugBsshListInq"
DETAIL_ENDPOINT = "getDrugBsshItemInq"
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
APP_DATA_DIR = LOCALAPPDATA / APP_NAME
LOG_DIR = APP_DATA_DIR / "logs"
SETTINGS_PATH = APP_DATA_DIR / "settings.json"
CREDENTIAL_PATH = APP_DATA_DIR / "credentials.dat"
PAGE_SIZE_OPTIONS = [10, 50, 100, 200, 500, 999]
MAX_SAFE_PAGES = 10000
REQUEST_DELAY_SECONDS = 0.15
