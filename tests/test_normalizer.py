from app.utils.company_normalizer import normalize_company_name
from app.utils.date_utils import parse_prmisn_date
from app.utils.address_utils import combine_factory_address, parse_address
def test_cleaning():
    assert normalize_company_name("하나제약㈜") == "하나제약"
    assert normalize_company_name("주식회사 한빛") == "한빛"
    assert parse_prmisn_date("19880509") == ("1988-05-09", True)
    assert parse_prmisn_date("19881340") == ("19881340", False)
    assert combine_factory_address("A", "B") == "A B"
    assert parse_address("강원도 춘천시 중앙로")[0] == "강원도"
