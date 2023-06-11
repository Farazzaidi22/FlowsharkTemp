from django.contrib import admin
from .models import Ticker

# Register your models here.
admin.site.site_title = "theFlowSharks"
admin.site.site_header = "theFlowSharks"

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ("name", "exchange", "sector", "industry", "country", "market_cap", "avg_volume", "ipo_date")
