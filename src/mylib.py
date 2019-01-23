from requests import get
from bs4 import BeautifulSoup


def st(tag):
    return tag.text.strip()


def pull_prices(company):
    url = f"https://www.nasdaq.com/symbol/{company}/historical"

    response = get(url)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        try:
            trs_soup = html_soup.find(id="historicalContainer").find("tbody").find_all(
                'tr')
            # print(len(chunk))
            rows = []
            for row in trs_soup:
                row = row.find_all('td')
                rows.append({
                    'Date': st(row[0]), 'Open': st(row[1]),
                    'High': st(row[2]), 'Low': st(row[3]),
                    'Close/Last': st(row[3]), 'Volume': st(row[4]),
                })
        except AttributeError as e:
            raise Exception(
                'The table is not found, markup has changed: {}'.format(e))

        return rows
