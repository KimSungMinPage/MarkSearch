from app.services.api_parser import parse_company_response
def test_response_wrapper_array():
    r=parse_company_response('{"response":{"header":{"resultCode":"00"},"body":{"pageNo":1,"numOfRows":1,"totalCount":1,"items":{"item":[{"ENTRPS":"하나제약㈜","PRMISN_NO":"2389"}]}}}}')
    assert len(r.body.items)==1 and r.body.items[0].normalized_entrps=="하나제약"
def test_top_level_object_null():
    r=parse_company_response('{"header":{},"body":{"items":{"item":{"ENTRPS":null,"PRMISN_DT":"19880509"}}}}')
    assert r.body.items[0].entrps=="" and r.body.items[0].prmisn_date_display=="1988-05-09"
def test_no_data(): assert parse_company_response('{"response":{"header":{},"body":{"items":[]}}}').body.items == []
