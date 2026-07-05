from dataclasses import dataclass
@dataclass
class BasicStatistics:
    company_records:int=0; unique_companies:int=0; unique_permits:int=0; factories:int=0; factories_with_address:int=0; factories_with_phone:int=0; missing_company_name:int=0; missing_permit_no:int=0; missing_address:int=0; invalid_date:int=0; duplicates:int=0
