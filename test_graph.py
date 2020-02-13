# ANNOTATING MOST RECENT VALUE

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc

import numpy as np
import urllib.request
import datetime as dt

datasets = ['DJIADM2019',
            'TAIEXDG2019',
            'JGBSLDM2019',
            'JGBMDM2019',
            'JGBLDM2019',
            'MOTHEDM2019',
            'REITDM2019',
            'TPX30DM2019',
            'JN400DM2019',
            'TOPIXMDM2019',
            'NK225MDH2019',
            'JGBLMDM2019',
            'NKVIDG2019',
            'FTC50DF2019',
            'TAIEXDF2019',
            'NKVIDF2019',
            'NK225MDG2019',
            'NK225MDF2019',
            'DJIADH2019']


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def graph_data(stock):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    stock_price_url = 'https://www.quandl.com/api/v3/datasets/OSE/' + stock + '.csv?api_key=8BfzK6Jo82TP_mF4CCvz'
    source_code = urllib.request.urlopen(stock_price_url).read().decode()
    # 'urllib.urlopen' for python 2.7
    stock_data = []
    split_source = source_code.split('\n')
    for line in split_source[1:]:
        split_line = line.split(',')
        if len(split_line) == 9:
            if 'values' not in line and 'label' not in line:
                stock_data.append(line)

    date, open, high, low, last, change, volume, sett_price, open_int = np.genfromtxt(stock_data,
                                                                                      delimiter=',',
                                                                                      unpack=True,
                                                                                      converters={0: bytespdate2num(
                                                                                          '%Y-%m-%d')})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], open[x], high[x], low[x], last[x], change[x], volume[x], sett_price[x], open_int[x]
        ohlc.append(append_me)
        x += 1

    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='g', colordown='r', alpha=0.5)

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)

    bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)
    ax1.annotate(str(last[-1]), (date[-1], last[-1]), xytext=(date[-1] + 3, last[-1]), bbox=bbox_props)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock)
    plt.subplots_adjust(left=0, bottom=0, right=0.87, top=1.5, wspace=0, hspace=0)
    plt.show()


for dataset in datasets:
    graph_data(dataset)