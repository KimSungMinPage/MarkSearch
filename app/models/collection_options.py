from dataclasses import dataclass
from enum import Enum
class KeyMode(str, Enum): AUTO="자동 감지"; DECODING="Decoding 인증키"; ENCODING="Encoding 인증키"
class CollectionKind(str, Enum): COMPANIES="업체 목록만"; FACTORIES="제조소 상세정보만"; BOTH="업체 목록과 제조소 상세정보 모두"
@dataclass
class CollectionOptions:
    service_key: str = ""; key_mode: KeyMode = KeyMode.AUTO; kind: CollectionKind = CollectionKind.BOTH; induty: str = ""; entrps: str = ""; prmisn_dt: str = ""; prmisn_no: str = ""; num_of_rows: int = 100; response_type: str = "json"
