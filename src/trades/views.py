import os
import json
from decimal import Decimal, DecimalException

from django.http import JsonResponse
from django.shortcuts import render
from django.core.management import call_command
from django.core.management.commands import flush
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

import locale
from datetime import datetime

from django_tables2 import RequestConfig

from tochka.settings import TICKERS_FILE, BASE_DIR, PROJECT_ROOT
from trades.mylib import parse_insider_trades, parse_prices
from .forms import DatesForm, DeltaForm
from .tables import StockPriceTable, TradeTable
from .serializers import StockPriceSerializer, TradeSerializer

from .models import Owner,  Company, Relation, Trade, StockPrice

# Create your views here.


def home(request):
    context = {}
    print(BASE_DIR, PROJECT_ROOT)
    return render(request, 'trades/base.html', context)


def insider(request, company, api=None):
    context = {}
    trades = Trade.objects.filter(company__name=company).order_by('-last_date')
    if api == 'api':
        serializer = TradeSerializer(trades, many=True)
        return JsonResponse(serializer.data, safe=False)

    table = TradeTable(trades)
    RequestConfig(request).configure(table)
    context.update(trades=table)
    return render(request, 'trades/insider_trades.html', context)


def insider_name(request, company, name, api=None):
    context = {}
    name = name.replace('_', ' ')
    trades = Trade.objects.filter(
        company__name=company, insider__name=name
    ).order_by('-last_date')
    if api == 'api':
        serializer = TradeSerializer(trades, many=True)
        return JsonResponse(serializer.data, safe=False)

    table = TradeTable(trades)
    RequestConfig(request).configure(table)
    context.update(trades=table)
    return render(request, 'trades/insider_trades.html', context)


def ticker(request, company, api=None):
    """Отображает страницу контактов

    Контексты:
    form (object): форма для отправки сообщений пользователями
    flag (bool):  если True то форма на странице не показывается
    """
    date_form = DatesForm(request.GET or None)
    delta_form = DeltaForm(request.GET or None)
    context = {}
    prices = StockPrice.objects.filter(company__name=company).order_by('-date')
    if date_form.is_valid():
        date_from = date_form.cleaned_data.get('date_from')
        date_to = date_form.cleaned_data.get('date_to')
        prices = prices.filter(date__gte=date_from, date__lte=date_to)
    if delta_form.is_valid():
        value = delta_form.cleaned_data.get('value')
        type = delta_form.cleaned_data.get('type')
    if api == 'api':
        serializer = StockPriceSerializer(prices, many=True)
        return JsonResponse(serializer.data, safe=False)

    table = StockPriceTable(prices)
    RequestConfig(request).configure(table)
    context.update(
        prices=table, company=company,
        date_form=date_form, delta_form=delta_form
    )

    return render(request, 'trades/tickers.html', context)

def ticker_analytics(request, company, api=None):


def date_parse(text):
    try:
        return datetime.strptime(text, '%m/%d/%Y').date()
    except ValueError:
        return datetime.now().date()


def parse_nasdaq(request):
    prices_data = None
    insider_trades_data = None
    context = {}
    result = {
        'success': True,
        'message': 'parse_nasdaq view is called!'
    }

    tickers_file = TICKERS_FILE
    with open(tickers_file) as f:
        content = f.readlines()
    companies = [x.strip().lower() for x in content]
    try:
        prices_data = parse_prices(companies, 10)
    except TypeError as e:
        error = f'prices parsing failed: {e}'
        result.update(success=False, message=error)
    try:
        insider_trades_data = parse_insider_trades(companies, 10)
    except TypeError as e:
        error = f'prices parsing failed: {e}'
        result.update(success=False, message=error)

    if prices_data:
        # truncate all tables
        cmd = flush.Command()
        call_command(cmd, verbosity=0, interactive=False)
        for company, rows in prices_data.items():
            company_obj = Company.objects.create(name=company)
            for row in rows:
                StockPrice.objects.create(
                    company=company_obj,
                    date=date_parse(row[0]),
                    open=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    volume=int(row[5].replace(',', ''))
                )
            # let's create insider trades for this company
            if insider_trades_data:
                for row in insider_trades_data[company]:
                    owner_obj, owner_created = Owner.objects.get_or_create(
                        name=row[0]
                    )
                    if owner_created:
                        Relation.objects.create(
                            position=row[1],
                            owner=owner_obj,
                            company=company_obj
                        )
                    try:
                        last_price = Decimal(row[6])
                    except DecimalException:
                        last_price = None

                    Trade.objects.create(
                        company=company_obj,
                        insider=owner_obj,
                        last_date=date_parse(row[2]),
                        transaction_type=row[3],
                        owner_type=row[4],
                        shares_traded=int(row[5].replace(',', '')),
                        last_price=last_price,
                        shares_held=int(row[7].replace(',', ''))
                    )

    print('Done!')
    return JsonResponse(result)
    # return render(request, 'trades/base.html', context)
