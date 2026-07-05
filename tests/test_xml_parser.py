from app.services.api_parser import parse_company_response, parse_factory_response
def test_normal_company_xml():
    r=parse_company_response('<response><header><resultCode>00</resultCode></header><body><totalCount>1</totalCount><items><item><ENTRPS>한빛</ENTRPS><ADRES>경기도 화성시 향남읍</ADRES></item></items></body></response>')
    assert r.body.items[0].sido == "경기도"
def test_factory_xml():
    r=parse_factory_response('<response><header><resultCode>00</resultCode></header><body><items><item><FCTRY_ADDR1>서울특별시 강남구</FCTRY_ADDR1><FCTRY_ADDR2>테헤란로</FCTRY_ADDR2><TELNO>010</TELNO></item></items></body></response>')
    assert r.body.items[0].combined_address == "서울특별시 강남구 테헤란로" and r.body.items[0].telno == "010"
def test_auth_error_xml():
    r=parse_company_response('<OpenAPI_ServiceResponse><cmmMsgHeader><errMsg>SERVICE ERROR</errMsg><returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg><returnReasonCode>30</returnReasonCode></cmmMsgHeader></OpenAPI_ServiceResponse>')
    assert not r.is_success and "등록되지" in r.header.result_msg
def test_empty_items(): assert parse_company_response('<response><header/><body><items/></body></response>').body.items == []
