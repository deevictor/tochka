from django.db import connection
from django.db.models import Sum
from requests import get
from bs4 import BeautifulSoup
from multiprocessing import Pool

from tochka.settings import SQL_FILE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(HTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
}


def parse_table(url, rows_selector):
    response = get(url, headers=HEADERS, timeout=15)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        try:
            rows_soup = html_soup.select(rows_selector)
            rows_list = []
            # for row in rows_soup:
            #     if row.select('td')[0].text.strip():
            #         rows_list.append(
            #             [v.text.strip() for v in row.select('td')]
            #         )
            rows_list = [[
                v.text.strip() for v in row.select('td')
            ] for row in rows_soup if row.select('td')[0].text.strip()]

        except AttributeError as e:
            raise Exception(
                'The table is not found, markup has changed: {}'.format(e)
            )
        except ConnectionError as e:
            raise Exception(
                'Make sure you are connected to Internet: {}'.format(e)
            )
        except TimeoutError as e:
            raise Exception(
                'Timeout Error: {}'.format(e)
            )

        return rows_list


def get_prices(company):
    url = f"https://www.nasdaq.com/symbol/{company}/historical"
    selector = 'div.genTable table tbody tr'
    rows_list = parse_table(url, selector)

    return {company: rows_list}


def parse_prices(companies, n):
    with Pool(n) as p:
        prices = p.map(get_prices, companies)

    prices_dict = {}
    for subdict in prices:
        prices_dict.update(
            {company: rows for company, rows in subdict.items()}
        )
    return prices_dict


def get_pages(company):
    url = f"https://www.nasdaq.com/symbol/{company}/insider-trades"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(HTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    }
    response = get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        try:
            # lets find out the number of the last page
            last_page_url = html_soup.find(
                'a', id='quotes_content_left_lb_LastPage'
            )['href']
            last_page_number = int(last_page_url[last_page_url.index('=')+1:])
            last_page_taken = last_page_number if last_page_number < 10 else 10
            pages = [url+f'?page={n}' for n in range(1, last_page_taken+1)]
        except AttributeError as e:
            raise Exception(
                'The table is not found, markup has changed: {}'.format(e)
            )
        except ConnectionError as e:
            raise Exception(
                'Make sure you are connected to Internet: {}'.format(e)
            )
        except TimeoutError as e:
            raise Exception(
                'Timeout Error: {}'.format(e)
            )

        return pages


def get_insider_trades(company):
    rows_selector = 'div.genTable table thead ~ tr'
    pages = get_pages(company)
    table = []
    # [table.extend(parse_table(page, rows_selector)) for page in pages]
    for page in pages:
        table.extend(parse_table(page, rows_selector))

    return {company: table}


def parse_insider_trades(companies, n):
    with Pool(n) as p:
        insider_trades = p.map(get_insider_trades, companies)

    insider_trades_dict = {}
    for subdict in insider_trades:
        insider_trades_dict.update(
            {company: rows for company, rows in subdict.items()}
        )

    return insider_trades_dict


data = [
    2, -10, 3, 15, 7, -1, -6, 10, 7, -4, 2, 9, 1, 0, -5, 0, 9, -2, -5, 1, 10
]
# n = 28
n = 2
result = []
desired_output = [3, 15, 7, -1, -6, 10]


def get_min_len(data, n, type):
    data = sorted(list(data.values('id', type)), key=lambda e: e[type])
    # data1.sort(key=keyfunc)
    orig_pos = len(data)-1
    pos = orig_pos
    total = 0
    for obj in data:
        total += obj[type]
        pos -= 1
        if total >= n:
            break
    return orig_pos - pos


def get_min_sets(qs, n, type):
    min_set_size = 999999
    min_set_possible = get_min_len(qs, n, type)
    data = list(qs.values('id', type))
    for start_pos in range(len(data) - min_set_possible):
        for end_pos in range(start_pos, len(data)-1):
            # total = sum(data[start_pos:end_pos+1])
            total = sum([e[type] for e in data[start_pos:end_pos+1]])
            set_size = end_pos + 1 - start_pos
            # if size of a set is less then min_size of a saved set then this
            # set is a new minimal set
            if set_size > min_set_size:
                break
            elif total >= n:
                if set_size < min_set_size:
                    # the size of the set is smaller then we have in result
                    min_set_size = set_size
                    result.clear()
                result.append(data[start_pos:end_pos+1])
                break

    return result


def get_sets_sql():
    file_sql = SQL_FILE
    with connection.cursor() as cursor:
        with open(file_sql) as f:
            content = f.read()
        f_content = content.format(threshold=15, company_id=1, val_type='open')
        cursor.execute(f_content)
        rows = cursor.fetchall()
    return rows
