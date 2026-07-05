import threading
from app.models import ApiResponse, ApiHeader, ApiBody
from app.services.collection_service import collect_pages
def test_collect_stops_last_page():
    def fetch(p): return ApiResponse(ApiHeader(), ApiBody(p, 2, 3, [p] if p<3 else [p]))
    assert collect_pages(fetch,2) == [1,2]
def test_cancel_event():
    ev=threading.Event(); ev.set();
    def fetch(p): return ApiResponse(ApiHeader(), ApiBody(p, 1, 2, [1]))
    assert collect_pages(fetch,1,ev) == [1]
def test_repeated_data_stops():
    def fetch(p): return ApiResponse(ApiHeader(), ApiBody(p, 1, 3, [1]))
    assert collect_pages(fetch,1) == [1]
