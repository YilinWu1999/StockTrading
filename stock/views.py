from django.shortcuts import render
import tushare as ts
from datetime import date, timedelta
import time
from stock.models import StockTable
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
        for i in range(0, len(stocks)):
            stock_ts = stocks.loc[i, 'ts_code']
            stock_symbol = stocks.loc[i, 'symbol']
            stock_name = stocks.loc[i, 'name']
            stock_industry = stocks.loc[i, 'industry']
            stock_market = stocks.loc[i, 'market']
            stock_list_date = stocks.loc[i, 'list_date']

            try:
                stock = StockTable.objects.filter(stock_ts=stock_ts)
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
        return render(request,'index.html')

def stock_all(request):
    if request.method == 'GET':
        stock_data = StockTable.objects.all()
        stocks=[]
        for i in range(0, len(stock_data)):
            stock={}
            stock['ts'] = stock_data[i].stock_ts
            stock['symbol'] = stock_data[i].stock_symbol
            stock['name'] = stock_data[i].stock_name
            stock['industry'] = stock_data[i].stock_industry
            stock['market'] = stock_data[i].stock_market
            stock['list_date'] = stock_data[i].stock_list_date
            stocks.append(stock)
        return render(request, 'stock_all.html', locals())

def stock_daily():
