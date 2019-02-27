from datetime import datetime
from decimal import Decimal, DecimalException

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.management import call_command
from django.core.management.commands import flush
from django_tables2 import RequestConfig

from tochka.settings import TICKERS_FILE, BASE_DIR, PROJECT_ROOT
from trades.mylib import parse_insider_trades, parse_prices, get_sets_sql
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

    if api == 'api':
        serializer = StockPriceSerializer(prices, many=True)
        return JsonResponse(serializer.data, safe=False)

    table = StockPriceTable(prices)

    if date_form.is_valid() and 'date_form' in request.GET:
        date_from = date_form.cleaned_data.get('date_from')
        date_to = date_form.cleaned_data.get('date_to')
        response = redirect('trades:ticker_analytics', company=company)
        response['Location'] += f'?date_from={date_from}&date_to={date_to}'
        return response

    if delta_form.is_valid()and 'delta_form' in request.GET:
        value = delta_form.cleaned_data.get('value')
        type = delta_form.cleaned_data.get('type')
        response = redirect('trades:ticker_delta', company=company)
        response['Location'] += f'?value={value}&type={type}'
        return response
    context.update(
        prices=table, company=company,
        date_form=date_form, delta_form=delta_form
    )
    return render(request, 'trades/tickers.html', context)


def ticker_delta(request, company, api=None):
    context = {}
    delta_form = DeltaForm(request.GET or None)
    tables = None
    if delta_form.is_valid():
        value = abs(delta_form.cleaned_data.get('value'))
        type = delta_form.cleaned_data.get('type')
        company_id = Company.objects.get(name=company).id
        rows = get_sets_sql(value, company_id, type)
        query_sets = [
            StockPrice.objects.filter(
                id__gte=row.startid, id__lte=row.startid + row.setsize
            ).order_by('-date') for row in rows
        ]
        if api == 'api':
            serializers = [
                StockPriceSerializer(qs, many=True).data for qs in query_sets
            ]
            return JsonResponse(serializers, safe=False)
        tables = [StockPriceTable(qs) for qs in query_sets]
    context.update(
        tables=tables, delta_form=delta_form, company=company
    )
    return render(request, 'trades/tickers.html', context)


def ticker_analytics(request, company, api=None):
    context = {}
    date_form = DatesForm(request.GET or None)
    prices = StockPrice.objects.filter(company__name=company).order_by(
        '-date'
    )
    if date_form.is_valid():
        date_from = date_form.cleaned_data.get('date_from')
        date_to = date_form.cleaned_data.get('date_to')
        prices = prices.filter(
            date__gte=date_from, date__lte=date_to
        ).order_by('-date')
    if api == 'api':
        serializer = StockPriceSerializer(prices, many=True)
        return JsonResponse(serializer.data, safe=False)
    table = StockPriceTable(prices)
    context.update(prices=table, date_form=date_form, company=company)
    return render(request, 'trades/tickers.html', context)


def date_parse(text):
    try:
        return datetime.strptime(text, '%m/%d/%Y').date()
    except ValueError:
        return datetime.now().date()


def parse_nasdaq(request):
    prices_data = None
    insider_trades_data = None
    context = {}
    result = {'message': 'Parsing is finished!'}

    tickers_file = TICKERS_FILE
    with open(tickers_file) as f:
        content = f.readlines()
    companies = [x.strip().lower() for x in content]
    try:
        prices_data = parse_prices(companies, 10)
    except TypeError as e:
        error = f'prices parsing failed: {e}'
        result.update(message=error)
    try:
        insider_trades_data = parse_insider_trades(companies, 10)
    except TypeError as e:
        error = f'prices parsing failed: {e}'
        result.update(message=error)

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

    return JsonResponse(result)

