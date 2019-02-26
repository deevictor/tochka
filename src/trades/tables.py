import django_tables2 as tables
from .models import StockPrice, Trade
# from .views import insider_name


class StockPriceTable(tables.Table):
    class Meta:
        model = StockPrice
        fields = ('date', 'open', 'high', 'low', 'close', 'volume')


# class UrlColumn(tables.Column):
#     def render(self, value):
#         return


class TradeTable(tables.Table):
    insider = tables.Column(
        linkify=("trades:insider_name", {
            "company": tables.A("company"),
            "name": tables.A("insider"),
        })
    )

    class Meta:
        model = Trade
        fields = (
            'insider', 'relation', 'last_date', 'transaction_type',
            'owner_type', 'shares_traded', 'shares_held'
                  )
