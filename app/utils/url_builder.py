from urllib.parse import urlencode, quote
from app.constants import BASE_URL, LIST_ENDPOINT, DETAIL_ENDPOINT
from app.models.collection_options import CollectionOptions, KeyMode
ENCODED_MARKERS = ("%2B", "%2F", "%3D", "%25")
def looks_encoded(key: str) -> bool:
    upper = key.upper(); return any(m in upper for m in ENCODED_MARKERS)
def _is_encoded_key(options: CollectionOptions) -> bool:
    return options.key_mode == KeyMode.ENCODING or (options.key_mode == KeyMode.AUTO and looks_encoded(options.service_key.strip()))
def build_url(endpoint: str, options: CollectionOptions, page_no: int) -> str:
    key = options.service_key.strip()
    params: dict[str, str | int] = {"pageNo": page_no, "numOfRows": options.num_of_rows, "type": options.response_type}
    if endpoint == LIST_ENDPOINT:
        if options.induty.strip(): params["Induty"] = options.induty.strip()
        if options.entrps.strip(): params["Entrps"] = options.entrps.strip()
        if options.prmisn_dt.strip(): params["Prmisn_dt"] = options.prmisn_dt.strip()
    elif endpoint == DETAIL_ENDPOINT and options.prmisn_no.strip():
        params["Prmisn_no"] = options.prmisn_no.strip()
    query = urlencode(params, doseq=False)
    service = key if _is_encoded_key(options) else quote(key, safe="")
    return f"{BASE_URL}/{endpoint}?serviceKey={service}&{query}"
def total_pages(total_count: int, num_of_rows: int) -> int:
    return 0 if total_count <= 0 or num_of_rows <= 0 else (total_count + num_of_rows - 1) // num_of_rows
