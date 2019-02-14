from requests import get
from bs4 import BeautifulSoup
from multiprocessing import Pool

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
            rows_list = [[
                v.text.strip() for v in row.select('td')
            ] for row in rows_soup]
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
    return prices


def get_pages(company):
    url = f"https://www.nasdaq.com/symbol/{company}/insider-trades"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
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
    table = [parse_table(page, rows_selector) for page in pages]

    return {company: table}


def parse_insider_trades(companies, n):
    with Pool(n) as p:
        insider_trades = p.map(get_insider_trades, companies)

    return insider_trades
