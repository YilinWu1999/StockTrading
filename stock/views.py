from django.shortcuts import render,redirect
import tushare as ts
import pandas as pd
from datetime import date, timedelta
import time
from stock.models import *
# Create your views here.


#获取前num的龙虎榜数据，num==0获取所有龙虎榜

def stock_top(num):
    ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
    pro = ts.pro_api()
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    data = pro.top_list(trade_date=yesterday)

    stocks = []
    if num == 0 :
        num=len(data)

    for i in range(0, num):
        stock = {}
        stock['ts_code'] = data.loc[i, 'ts_code']
        stock['name'] = data.loc[i, 'name']
        stock['pct_change'] = data.loc[i, 'pct_change']
        stock['reason'] = data.loc[i, 'reason']
        stocks.append(stock)
    return stocks

def stock_update(request):
    if request.method == 'GET':
        # 获取/更新当前上市交易的股票信息
        ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
        pro = ts.pro_api()
        stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,market,industry,list_date')
        print(stocks)
        for i in range(0, len(stocks)):
            stock_ts = stocks.loc[i, 'ts_code']
            stock_symbol = stocks.loc[i, 'symbol']
            stock_name = stocks.loc[i, 'name']
            stock_industry = stocks.loc[i, 'industry']
            stock_market = stocks.loc[i, 'market']
            stock_list_date = stocks.loc[i, 'list_date']

            try:
                stock = StockTable.objects.get(stock_ts=stock_ts)
                if stock:
                    stock.stock_ts = stock_ts
                    stock.stock_symbol = stock_symbol
                    stock.stock_name = stock_name
                    stock.stock_industry = stock_industry
                    stock.stock_market = stock_market
                    stock.stock_list_date = stock_list_date
                else:
                    stock = StockTable.objects.create(
                        stock_ts=stock_ts,
                        stock_symbol=stock_symbol,
                        stock_name=stock_name,
                        stock_industry=stock_industry,
                        stock_market=stock_market,
                        stock_list_date=stock_list_date,
                    )
                stock.save()
            except Exception:
                print(Exception)
                print('1111111')
        return redirect('index')

def stock_all(request):
    if request.method == 'GET':
        #stock_daily_update('today_all')
        today = date.today().strftime("%Y-%m-%d")
        print()
        stock_data = StockTable.objects.all()
        stocks=[]
        for i in range(0, len(stock_data)):
            stock={}
            try:
                stock_daily_data = StockDailyTable.objects.get(stock_ts=stock_data[i].stock_ts,stock_daily_date=today)
            except:
                continue
            stock['ts'] = stock_data[i].stock_ts
            stock['symbol'] = stock_data[i].stock_symbol
            stock['name'] = stock_data[i].stock_name
            stock['close'] = stock_daily_data.stock_daily_close
            stock['change'] = stock_daily_data.stock_daily_change
            stock['pct'] = stock_daily_data.stock_daily_pct
            stocks.append(stock)
        return render(request, 'stock_all.html', locals())


# ts_code 	str 	股票代码
# trade_date 	str 	交易日期
# open 	float 	开盘价
# high 	float 	最高价
# low 	float 	最低价
# close 	float 	收盘价
# pre_close 	float 	昨收价
# change 	float 	涨跌额
# pct_chg 	float 	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
# vol 	float 	成交量 （手）
# amount 	float 	成交额 （千元）
def stock_daily_update(option):
        # 获取股票日线信息
        ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
        pro = ts.pro_api()
        data = pd.DataFrame()
        if option == 'today_all':
            today = date.today().strftime("%Y%m%d")
            data = pro.daily(trade_date=today)
            print(data)
            for i in range(0,len(data)):
                stock_ts = data.loc[i, 'ts_code']
                stock_daily_date = pd.to_datetime(data.loc[i, 'trade_date'])
                stock_daily_open = data.loc[i, 'open']
                stock_daily_high = data.loc[i, 'high']
                stock_daily_low = data.loc[i, 'low']
                stock_daily_close = data.loc[i, 'close']
                stock_daily_pclose = data.loc[i, 'pre_close']
                stock_daily_change = data.loc[i, 'change']
                stock_daily_pct = data.loc[i, 'pct_chg']
                stock_daily_vol = data.loc[i, 'vol']
                stock_daily_amount = data.loc[i, 'amount']
                try:
                    stock = StockTable.objects.get(stock_ts=stock_ts)
                except Exception as e:
                    print(stock_ts+'该股还未上市')
                if StockDailyTable.objects.filter(stock_ts=stock_ts,stock_daily_date=stock_daily_date):
                    continue;
                try:
                    stock_daily = StockDailyTable.objects.create(
                        stock_ts = stock_ts,
                        stock_daily_date = stock_daily_date,
                        stock_daily_open = stock_daily_open,
                        stock_daily_high = stock_daily_high,
                        stock_daily_low = stock_daily_low,
                        stock_daily_close = stock_daily_close,
                        stock_daily_pclose = stock_daily_pclose,
                        stock_daily_change = stock_daily_change,
                        stock_daily_pct = stock_daily_pct,
                        stock_daily_vol = stock_daily_vol,
                        stock_daily_amount = stock_daily_amount,
                        stock = stock
                    )
                    stock_daily.save()
                except Exception as e:
                    print('个股日线信息获取失败')
                    print(e)



