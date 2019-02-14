import time

from mylib import parse_insider_trades, parse_prices


# companies = ['aapl', 'cvx', 'goog']
companies = ['aapl', ]
t = time.process_time()
insider_trades_data = parse_insider_trades(companies, 10)
prices_data = parse_prices(companies, 10)
elapsed_time = time.process_time() - t
print(elapsed_time)
print('DONE')
