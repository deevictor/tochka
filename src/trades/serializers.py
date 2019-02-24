from rest_framework import serializers

from .models import StockPrice, Trade


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ('date', 'open', 'high', 'low', 'close', 'volume')


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            'insider', 'relation', 'last_date', 'transaction_type',
            'owner_type', 'shares_traded', 'shares_held'
                  )
