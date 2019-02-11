from mylib import pull_prices


companies = ['aapl',]
data = []
for company in companies:
    data.append(pull_prices(company))

print(data)