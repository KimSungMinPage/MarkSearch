from collections import Counter
from app.models import Company, Factory, BasicStatistics
class StatisticsService:
    def basic(self, companies: list[Company], factories: list[Factory]) -> BasicStatistics:
        return BasicStatistics(len(companies), len({c.normalized_entrps for c in companies if c.normalized_entrps}), len({c.prmisn_no for c in companies if c.prmisn_no}), len(factories), sum(bool(f.combined_address) for f in factories), sum(bool(f.telno) for f in factories), sum(not c.entrps for c in companies)+sum(not f.entrps for f in factories), sum(not c.prmisn_no for c in companies)+sum(not f.prmisn_no for f in factories), sum(not c.adres for c in companies)+sum(not f.combined_address for f in factories), sum((not c.is_valid_date and bool(c.prmisn_dt)) for c in companies)+sum((not f.is_valid_date and bool(f.prmisn_dt)) for f in factories), sum(c.is_duplicate for c in companies)+sum(f.is_duplicate for f in factories))
    def industry_counts(self, companies:list[Company], factories:list[Factory]) -> list[tuple[str,int,int]]:
        c = Counter(x.induty or "미상" for x in companies); f = Counter(x.induty or "미상" for x in factories); return [(k,c[k],f[k]) for k in sorted(set(c)|set(f))]
    def region_counts(self, companies:list[Company], factories:list[Factory]) -> list[tuple[str,int,int]]:
        c = Counter(x.sido or "미상" for x in companies); f = Counter(x.sido or "미상" for x in factories); return [(k,c[k],f[k]) for k in sorted(set(c)|set(f))]
