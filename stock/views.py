import os

from django.core.paginator import Paginator
from django.shortcuts import render,redirect
import tushare as ts
import pandas as pd
from datetime import date, timedelta
import time

from StockTrading.settings import BASE_DIR
from stock.models import *
from pyecharts.charts import Kline
import pyecharts.options as opts
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
        today = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        stock_data = StockTable.objects.all()
        stock_daily_data = StockDailyTable.objects.filter(stock_daily_date=today)
        stocks=[]
        for i in range(0, len(stock_data)):
            stock={}
            stock['ts'] = stock_data[i].stock_ts
            stock['symbol'] = stock_data[i].stock_symbol
            stock['name'] = stock_data[i].stock_name
            try:
                stock_daily = stock_daily_data.get(stock_ts=stock['ts'])
                stock['close'] = stock_daily.stock_daily_close
                stock['change'] = stock_daily.stock_daily_change
                stock['pct'] = stock_daily.stock_daily_pct
            except:
                stock['close'] = 0
                stock['change'] = 0
                stock['pct'] = 0

            stocks.append(stock)
        # page_num = request.GET.get('page',1)
        # paginator = Paginator(stocks,20)
        # c_page = paginator.page(int(page_num))
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

def stock_detail(request):
    # 载入tushare
    ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
    pro = ts.pro_api()
    symbol = request.GET['symbol']
    stock = StockTable.objects.get(stock_symbol=symbol)
    ts_code = stock.stock_ts

    # 生成日K线
    # 获取需要显示的日线数据  50天的日线数据
    end_date = date.today().strftime("%Y%m%d")
    start_date = (date.today() + timedelta(days=-50)).strftime("%Y%m%d")
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    # 将交易日期设计为索引
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    v1 = list(df.loc[:, ['open', 'close', 'low', 'high']].values.tolist())
    t = df.index
    v0 = list(t.strftime('%Y/%m/%d'))
    daily = (
        Kline()
            .add_xaxis(v0)
            .add_yaxis("kline", v1)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title=symbol+" "+stock.stock_name+" "+"日K线图"),
        )
            .render('./templates/daily_kline.html')
    )

    # 生成周K线
    end_date = date.today().strftime("%Y%m%d")
    start_date = (date.today() + timedelta(days=-350)).strftime("%Y%m%d")
    df = pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    # 将交易日期设计为索引
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    v1 = list(df.loc[:, ['open', 'close', 'low', 'high']].values.tolist())
    t = df.index
    v0 = list(t.strftime('%Y/%m/%d'))
    daily = (
        Kline()
            .add_xaxis(v0)
            .add_yaxis("kline", v1)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title=symbol+" "+stock.stock_name+" "+"周K线图"),
        )
            .render('./templates/week_kline.html')
    )

    # 生成月K线
    end_date = date.today().strftime("%Y%m%d")
    start_date = (date.today() + timedelta(days=-1500)).strftime("%Y%m%d")
    df = pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    # 将交易日期设计为索引
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    v1 = list(df.loc[:, ['open', 'close', 'low', 'high']].values.tolist())
    t = df.index
    v0 = list(t.strftime('%Y/%m/%d'))
    daily = (
        Kline()
            .add_xaxis(v0)
            .add_yaxis("kline", v1)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title=symbol+" "+stock.stock_name+" "+"月K线图"),
        )
            .render('./templates/month_kline.html')
    )

    # 获取股票基本数据
    today = date.today()
    if today.weekday()==5:
        today = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    elif today.weekday()==6:
        today = (date.today() + timedelta(days=-2)).strftime("%Y%m%d")
    else:
        today = date.today().strftime("%Y%m%d")
    df = pro.daily_basic(ts_code=ts_code, trade_date=today,
                         fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,total_share,float_share,free_share,total_mv,circ_mv')
    stock_basic = {}
    stock_basic['name'] = stock.stock_name
    stock_basic['ts_code'] = df.loc[0, 'ts_code']
    stock_basic['trade_date'] = df.loc[0,'trade_date']
    stock_basic['close'] = df.loc[0,'close']
    stock_basic['turnover_rate'] = df.loc[0,'turnover_rate']
    stock_basic['volume_ratio'] = df.loc[0,'volume_ratio']
    stock_basic['pe'] = df.loc[0,'pe']
    stock_basic['pb'] = df.loc[0,'pb']
    stock_basic['total_share'] = df.loc[0,'total_share']
    stock_basic['float_share'] = df.loc[0,'float_share']
    stock_basic['free_share'] = df.loc[0,'free_share']
    stock_basic['total_mv'] = df.loc[0,'total_mv']
    stock_basic['circ_mv'] = df.loc[0,'circ_mv']
    df = pro.daily(ts_code=ts_code, start_date=today, end_date=today)
    stock_basic['high'] = df.loc[0, 'high']
    stock_basic['low'] = df.loc[0, 'low']
    stock_basic['vol'] = df.loc[0, 'vol']
    stock_basic['open'] = df.loc[0, 'open']
    stock_basic['amount'] = df.loc[0, 'amount']
    stock_basic['change'] = df.loc[0, 'change']
    stock_basic['pct_chg'] = df.loc[0, 'pct_chg']
    stock_basic['pre_close'] = df.loc[0, 'pre_close']

    # 获取股票财务信息
    df = pro.fina_indicator(ts_code=ts_code,period="20211231",fields='eps,bps,cfps,roe,undist_profit_ps,capital_rese_ps,profit_dedt,or_yoy,q_op_yoy,debt_to_assets,npta,gross_margin')
    stock_finance = {}
    stock_finance['eps'] = df.loc[0, 'eps']
    stock_finance['bps'] = df.loc[0, 'bps']
    stock_finance['cfps'] = df.loc[0, 'cfps']
    stock_finance['roe'] = df.loc[0, 'roe']
    stock_finance['undist_profit_ps'] = df.loc[0, 'undist_profit_ps']
    stock_finance['capital_rese_ps'] = df.loc[0, 'capital_rese_ps']
    stock_finance['profit_dedt'] = df.loc[0, 'profit_dedt']
    stock_finance['or_yoy'] = df.loc[0, 'or_yoy']
    stock_finance['q_op_yoy'] = df.loc[0, 'q_op_yoy']
    stock_finance['debt_to_assets'] = df.loc[0, 'debt_to_assets']
    stock_finance['npta'] = df.loc[0, 'npta']
    stock_finance['gross_margin'] = df.loc[0, 'gross_margin']

    return render(request,'stock_detail.html',locals())

def daily_kline(request):
    return render(request, 'daily_kline.html', {})

def week_kline(request):
    return render(request, 'week_kline.html', {})

def month_kline(request):
    return render(request, 'month_kline.html', {})

def stock_optional_add(request):
    if request.method == 'GET':

        return render(request,'stock_optional.html')
    elif request.method == 'POST':
        return render(request, 'stock_optional.html')

def stock_optional(request):
    return render(request,'')

def stock_optional_del(request):
    return render(request,'')