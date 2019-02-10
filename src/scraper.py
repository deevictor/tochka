from requests import get
from bs4 import BeautifulSoup

company = 'aapl'
url = f"https://www.nasdaq.com/symbol/{company}/historical"

response = get(url)
# print(response.text[:1000])
html_soup = BeautifulSoup(response.text, 'html.parser')
# lines = html_soup.find_all('')
chunk = html_soup.find(id="historicalContainer").find("tbody").find_all('tr')
print(type(chunk))
