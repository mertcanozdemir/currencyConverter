import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv


URL = "https://www.x-rates.com/table/?from=TRY&amount=1"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib

quotes = []  # a list to store quotes
currenciesTopTen = soup.find('table', attrs={'class': 'ratesTable'})
date = soup.find('span', attrs={'class': 'ratesTimestamp'}).text
currencies = soup.find('table', attrs={'class': 'tablesorter ratesTable'})


# print(date)

for row in currenciesTopTen.findAll('tr'):
    quote = {}
    quote['currency'] = row.find_next('td').text
    quote['rate'] = round(float(row.find_next('a').text), 2)
    quote['toTRY'] = round(1/float(row.find_next('a').text), 2)
    quote['RatesTimeStamp'] = date
    quotes.append(quote)

filename = 'currency.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['currency', 'rate', 'toTRY','RatesTimeStamp'])
    w.writeheader()
    for quote in quotes[1:]:
        w.writerow(quote)


read_file = pd.read_csv('./currency.csv')
read_file.to_excel('currency.xlsx', sheet_name="Exchange", index=False)
