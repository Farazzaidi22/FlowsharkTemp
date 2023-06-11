from django.db import models


# Create your models here.
class Ticker(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    exchange = models.CharField(max_length=120, blank=True, null=True)
    sector = models.CharField(max_length=120, blank=True, null=True)
    industry = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)
    market_cap = models.FloatField(blank=True, null=True)
    dividend_yield = models.FloatField(blank=True, null=True)
    analyst_recom = models.CharField(max_length=120, blank=True, null=True)
    earning_date = models.CharField(max_length=120, blank=True, null=True)
    avg_volume = models.FloatField(blank=True, null=True)
    relative_volume = models.FloatField(blank=True, null=True)
    current_volume = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    ipo_date = models.CharField(max_length=120, blank=True, null=True)
    float = models.FloatField(blank=True, null=True)
    outstanding_shares = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    forward_pe = models.FloatField(blank=True, null=True)
    peg = models.FloatField(blank=True, null=True)
    ps = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    price_cash = models.FloatField(blank=True, null=True)
    price_fcf = models.FloatField(blank=True, null=True)
    eps_growth_this_year = models.FloatField(blank=True, null=True)
    eps_growth_next_year = models.FloatField(blank=True, null=True)
    eps_growth_five_years = models.FloatField(blank=True, null=True)
    eps_growth = models.FloatField(blank=True, null=True)
    revenue_growth = models.FloatField(blank=True, null=True)
    return_on_assets = models.FloatField(blank=True, null=True)
    return_on_equity = models.FloatField(blank=True, null=True)
    current_ratio = models.FloatField(blank=True, null=True)
    quick_ratio = models.FloatField(blank=True, null=True)
    debt_equity = models.FloatField(blank=True, null=True)
    gross_margin = models.FloatField(blank=True, null=True)
    operating_margin = models.FloatField(blank=True, null=True)
    net_profit_margin = models.FloatField(blank=True, null=True)
    payout_ratio = models.FloatField(blank=True, null=True)
    institutional_ownership = models.FloatField(blank=True, null=True)
    d1 = models.FloatField(blank=True, null=True)
    d5 = models.FloatField(blank=True, null=True)
    m1 = models.FloatField(blank=True, null=True)
    m3 = models.FloatField(blank=True, null=True)
    m6 = models.FloatField(blank=True, null=True)
    ytd = models.FloatField(blank=True, null=True)
    y1 = models.FloatField(blank=True, null=True)
    y3 = models.FloatField(blank=True, null=True)
    y5 = models.FloatField(blank=True, null=True)
    y10 = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name 
    



