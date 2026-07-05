from app.models import CollectionOptions, KeyMode
from app.constants import LIST_ENDPOINT, DETAIL_ENDPOINT
from app.utils.url_builder import build_url, total_pages
def test_decoding_key_encoded(): assert "a%2Bb%2F%3D" in build_url(LIST_ENDPOINT, CollectionOptions(service_key="a+b/="), 1)
def test_encoding_key_not_double_encoded():
    url=build_url(LIST_ENDPOINT, CollectionOptions(service_key="a%2Bb%2F%3D", key_mode=KeyMode.ENCODING),1); assert "%252B" not in url and "a%2Bb%2F%3D" in url
def test_korean_and_empty_params():
    url=build_url(LIST_ENDPOINT, CollectionOptions(service_key="k", entrps="하나제약"),1); assert "Entrps=" in url and "Induty=" not in url
def test_date_and_permit_params():
    assert "Prmisn_dt=19880509" in build_url(LIST_ENDPOINT, CollectionOptions(service_key="k", prmisn_dt="19880509"),1)
    assert "Prmisn_no=2389" in build_url(DETAIL_ENDPOINT, CollectionOptions(service_key="k", prmisn_no="2389"),1)
def test_total_pages(): assert total_pages(3688,100)==37 and total_pages(0,100)==0
