import threading, time
from typing import Callable, TypeVar
from app.constants import MAX_SAFE_PAGES, REQUEST_DELAY_SECONDS
from app.models import ApiResponse
from app.utils.url_builder import total_pages
T = TypeVar('T')
def collect_pages(fetch: Callable[[int], ApiResponse[T]], num_of_rows: int, cancel_event: threading.Event | None = None, progress: Callable[[dict], None] | None = None) -> list[T]:
    cancel_event = cancel_event or threading.Event(); results: list[T] = []; last_signature = None; failures = 0; start = time.time()
    first = fetch(1)
    if not first.is_success: raise RuntimeError(first.header.result_msg)
    pages = total_pages(first.body.total_count, num_of_rows) or (1 if first.body.items else 0)
    for page, response in [(1, first)]:
        results.extend(response.body.items); _progress(progress, page, pages, len(results), response.body.total_count, start)
    last_signature = repr(first.body.items)
    for page_no in range(2, min(pages, MAX_SAFE_PAGES) + 1):
        if cancel_event.is_set(): break
        try:
            response = fetch(page_no); failures = 0
        except Exception:
            failures += 1
            if failures > 3: break
            continue
        signature = repr(response.body.items)
        if not response.body.items or signature == last_signature: break
        last_signature = signature; results.extend(response.body.items); _progress(progress, page_no, pages, len(results), response.body.total_count, start); time.sleep(REQUEST_DELAY_SECONDS)
    return results
def _progress(callback: Callable[[dict], None] | None, page:int, pages:int, count:int, total:int, start:float) -> None:
    if callback: callback({"current_page":page,"total_pages":pages,"received_count":count,"total_count":total,"elapsed":time.time()-start,"percent":0 if total<=0 else min(100,count*100/total)})
