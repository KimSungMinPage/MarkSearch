from app.models import Company, Factory
from app.utils.duplicate_detector import mark_duplicates
def test_company_duplicate():
    rows=[Company(prmisn_no="1",induty="A",entrps="B",adres="C"),Company(prmisn_no="1",induty="A",entrps="B",adres="C")]; mark_duplicates(rows); assert rows[0].is_duplicate and rows[1].duplicate_group_no == 1
def test_factory_duplicate():
    rows=[Factory(prmisn_no="1",sn="2",fctry_nm="F",fctry_addr1="A"),Factory(prmisn_no="1",sn="2",fctry_nm="F",fctry_addr1="A")]; mark_duplicates(rows); assert rows[0].is_duplicate
