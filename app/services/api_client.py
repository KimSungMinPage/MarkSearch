import time
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
try:
    import requests  # type: ignore
except Exception:
    requests = None
from app.constants import LIST_ENDPOINT, DETAIL_ENDPOINT
from app.models import CollectionOptions, ApiResponse, Company, Factory
from app.services.api_parser import parse_company_response, parse_factory_response
from app.utils.url_builder import build_url
RETRY_STATUS = {408,429,500,502,503,504}
class DataGoApiClient:
    def __init__(self, session: Any | None = None, timeout: int = 30) -> None:
        self.session = session or (requests.Session() if requests else None); self.timeout = timeout
    def get_company_page(self, options: CollectionOptions, page_no: int) -> ApiResponse[Company]:
        return parse_company_response(self._get(build_url(LIST_ENDPOINT, options, page_no)))
    def get_factory_page(self, options: CollectionOptions, page_no: int) -> ApiResponse[Factory]:
        return parse_factory_response(self._get(build_url(DETAIL_ENDPOINT, options, page_no)))
    def _get(self, url: str) -> str:
        last_error: Exception | None = None
        for attempt, delay in enumerate([0,1,2,4]):
            if delay: time.sleep(delay)
            try:
                if requests and self.session is not None:
                    response = self.session.get(url, timeout=self.timeout)
                    if response.status_code in RETRY_STATUS and attempt < 3: continue
                    response.raise_for_status(); response.encoding = response.encoding or "utf-8"; return response.text
                req = Request(url, headers={"User-Agent":"GmpCompanyCollector/1.0"})
                with urlopen(req, timeout=self.timeout) as res:
                    return res.read().decode(res.headers.get_content_charset() or "utf-8", errors="replace")
            except HTTPError as exc:
                last_error = exc
                if exc.code in RETRY_STATUS and attempt < 3: continue
                raise
            except (URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt >= 3: raise
        raise RuntimeError(str(last_error))
