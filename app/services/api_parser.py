import json, xml.etree.ElementTree as ET
from typing import Any, Callable, TypeVar
from app.models import ApiBody, ApiHeader, ApiResponse, Company, Factory
from app.utils.text_utils import clean_text
from app.utils.company_normalizer import normalize_company_name
from app.utils.date_utils import parse_prmisn_date
from app.utils.address_utils import parse_address, combine_factory_address
T = TypeVar('T')
ERROR_MESSAGES = {"1":"공공데이터 서버 처리 오류입니다. 잠시 후 다시 시도하십시오.","10":"요청 파라미터 오류입니다. 검색조건을 확인하십시오.","12":"OpenAPI가 존재하지 않거나 종료되었습니다.","20":"API 접근이 거부되었습니다. 활용신청 승인 여부를 확인하십시오.","22":"요청 한도를 초과했습니다.","30":"등록되지 않은 서비스키입니다. 인증키와 인코딩 형식을 확인하십시오.","31":"활용기간이 만료되었습니다.","32":"등록되지 않은 IP입니다.","99":"알 수 없는 서버 오류입니다."}
def error_message(code: str) -> str: return ERROR_MESSAGES.get(code, f"알 수 없는 오류입니다. 코드: {code}")
def parse_company_response(raw: str) -> ApiResponse[Company]: return _parse(raw, _map_company)
def parse_factory_response(raw: str) -> ApiResponse[Factory]: return _parse(raw, _map_factory)
def _parse(raw: str, mapper: Callable[[dict[str, Any]], T]) -> ApiResponse[T]:
    text = (raw or "").strip()
    if not text: raise ValueError("빈 응답입니다.")
    if text.startswith("<"): return _parse_xml(text, mapper)
    if text.startswith(("{", "[")): return _parse_json(text, mapper)
    raise ValueError(f"알 수 없는 응답 형식입니다: {text[:100]}")
def _parse_json(text: str, mapper: Callable[[dict[str, Any]], T]) -> ApiResponse[T]:
    data = json.loads(text)
    root = data.get("response", data) if isinstance(data, dict) else {}
    header = root.get("header", {}) or {}; body = root.get("body", {}) or {}
    items_node = body.get("items", [])
    if isinstance(items_node, dict) and "item" in items_node: items_node = items_node["item"]
    if isinstance(items_node, dict): rows = [items_node]
    elif isinstance(items_node, list): rows = items_node
    else: rows = []
    return ApiResponse(ApiHeader(clean_text(header.get("resultCode", "00")), clean_text(header.get("resultMsg", ""))), ApiBody(_to_int(body.get("pageNo")), _to_int(body.get("numOfRows")), _to_int(body.get("totalCount")), [mapper(r or {}) for r in rows]))
def _parse_xml(text: str, mapper: Callable[[dict[str, Any]], T]) -> ApiResponse[T]:
    root = ET.fromstring(text)
    err = root.find(".//cmmMsgHeader")
    if err is not None:
        code = clean_text(_child_text(err, "returnReasonCode")); return ApiResponse(ApiHeader(code, error_message(code), clean_text(_child_text(err, "errMsg")), clean_text(_child_text(err, "returnAuthMsg")), code), ApiBody())
    header_node = root.find(".//header"); body_node = root.find(".//body")
    header = ApiHeader(clean_text(_child_text(header_node, "resultCode") or "00"), clean_text(_child_text(header_node, "resultMsg")))
    rows = [] if body_node is None else [{c.tag: clean_text(c.text) for c in item} for item in body_node.findall(".//item")]
    body = ApiBody(_to_int(_child_text(body_node, "pageNo")), _to_int(_child_text(body_node, "numOfRows")), _to_int(_child_text(body_node, "totalCount")), [mapper(r) for r in rows])
    return ApiResponse(header, body)
def _child_text(node: ET.Element | None, name: str) -> str:
    found = None if node is None else node.find(name)
    return "" if found is None or found.text is None else found.text
def _to_int(value: Any) -> int:
    try: return int(value or 0)
    except (TypeError, ValueError): return 0
def _get(row: dict[str, Any], name: str) -> str: return clean_text(row.get(name, ""))
def _map_company(row: dict[str, Any]) -> Company:
    dt, valid = parse_prmisn_date(_get(row, "PRMISN_DT")); addr = _get(row, "ADRES"); sido, sigungu = parse_address(addr); entrps = _get(row, "ENTRPS")
    return Company(_get(row,"INDUTY"), entrps, normalize_company_name(entrps), _get(row,"RPRSNTV"), _get(row,"PRMISN_DT"), dt, valid, addr, _get(row,"PRMISN_NO"), sido, sigungu)
def _map_factory(row: dict[str, Any]) -> Factory:
    dt, valid = parse_prmisn_date(_get(row, "PRMISN_DT")); combined = combine_factory_address(_get(row,"FCTRY_ADDR1"), _get(row,"FCTRY_ADDR2")); sido, sigungu = parse_address(combined); entrps = _get(row,"ENTRPS")
    return Factory(entrps, normalize_company_name(entrps), _get(row,"INDUTY"), _get(row,"PRMISN_NO"), _get(row,"RPRSNTV"), _get(row,"PRMISN_DT"), dt, valid, _get(row,"SN"), _get(row,"FCTRY_NM"), _get(row,"TELNO"), _get(row,"FCTRY_ADDR1"), _get(row,"FCTRY_ADDR2"), combined, sido, sigungu)
