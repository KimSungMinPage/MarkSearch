from dataclasses import dataclass, field
from typing import Generic, TypeVar
T = TypeVar('T')
@dataclass
class ApiHeader:
    result_code: str = "00"; result_msg: str = "NORMAL SERVICE."; err_msg: str = ""; return_auth_msg: str = ""; return_reason_code: str = ""
    @property
    def is_success(self) -> bool: return self.result_code in ("00", "0", "") and not self.return_reason_code
@dataclass
class ApiBody(Generic[T]):
    page_no: int = 0; num_of_rows: int = 0; total_count: int = 0; items: list[T] = field(default_factory=list)
@dataclass
class ApiResponse(Generic[T]):
    header: ApiHeader; body: ApiBody[T]
    @property
    def is_success(self) -> bool: return self.header.is_success
