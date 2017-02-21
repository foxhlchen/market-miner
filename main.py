# http://q.stock.sohu.com/hisHq?code=cn_600008&start=19900101&end=20170220&stat=1&order=D&period=d

import urllib.request
import json
import time
from tqdm import *
import random
import os


def fetch_quote(ticker, from_date, to_date):
    url_templ = "http://q.stock.sohu.com/hisHq?code=cn_{}&start={}&end={}&stat=1&order=D&period=d"
    url = url_templ.format(ticker, from_date, to_date)
    page = urllib.request.urlopen(url)
    return str(page.read(), encoding="gbk")


def tocsv(jstr):
    q = json.loads(jstr)
    q = q[0]
    csv = []

    if q['status'] != 0:
        raise ValueError(q)

    hq = q['hq']
    csv.append('日期,开盘,收盘,涨跌额,涨跌幅,最低,最高,成交量(手),成交金额(万),换手率\n')
    for entry in hq:
        entry[4] = entry[4].replace('%', '')
        for i in range(9):
            csv.append(str(entry[i]))
            csv.append(',')
        csv.append(entry[9].replace('%', ''))
        csv.append('\n')

    return ''.join(csv)


if __name__ == '__main__':
    ticker_path = 'tickers.txt'
    csv_folder = './csv/'
    from_date = '19900101'
    to_date = time.strftime("%Y%m%d")

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    ticker_list = []
    ticker_file = open(ticker_path, 'r')
    for ticker in ticker_file:
        ticker = ticker.replace('\n', '')
        ticker = ticker.replace('\r', '')
        if len(ticker) > 0:
            ticker_list.append(ticker)

    for ticker in tqdm(ticker_list):
        # print(ticker)
        try:
            jstr = fetch_quote(ticker, from_date, to_date)
            csv_str = tocsv(jstr)
            # print(csv_str)
        except ValueError as v:
            print(v)

        with open(csv_folder + ticker + '.csv', 'w') as f:
            f.write(csv_str)

            # random_time = random.uniform(1, 3)
            # time.sleep(random_time)
