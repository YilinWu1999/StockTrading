from django.db import models

# Create your models here.

class StockTable(models.Model):
    # 股票信息表，记录股票系统中的股票信息
    # 股票ts代码
    stock_ts =  models.CharField(max_length=10, primary_key=True)
    # 股票代码，固定6位，PK
    stock_symbol = models.CharField(max_length=6)
    # 股票名称
    stock_name = models.CharField(max_length=50)
    # 股票行业
    stock_industry = models.CharField(max_length=45)
    # 股票所属市场类型
    stock_market = models.CharField(max_length=45)
    # 股票上市日期
    stock_list_date = models.CharField(max_length=45)

    def __str__(self):
        return '-'.join([self.stock_symbol, self.stock_name])

    class Meta:
        db_table = 'stock_table'



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
class StockDailyTable(models.Model):
    # 股票每日交易信息
    # 股票ts代码
    stock_ts = models.CharField(max_length=10)
    # 交易日期
    stock_daily_date = models.DateField()
    # 开盘价
    stock_daily_open = models.DecimalField(max_digits=6,decimal_places=2)
    # 最高价
    stock_daily_high = models.DecimalField(max_digits=6,decimal_places=2)
    # 最低价
    stock_daily_low = models.DecimalField(max_digits=6,decimal_places=2)
    # 收盘价
    stock_daily_close = models.DecimalField(max_digits=6,decimal_places=2)
    # 昨收价
    stock_daily_pclose = models.DecimalField(max_digits=6,decimal_places=2)
    # 涨跌额
    stock_daily_change = models.DecimalField(max_digits=6,decimal_places=2)
    # 涨跌幅
    stock_daily_pct = models.DecimalField(max_digits=6,decimal_places=2)
    # 成交量 单位手
    stock_daily_vol = models.DecimalField(max_digits=20,decimal_places=2)
    # 成交额
    stock_daily_amount = models.DecimalField(max_digits=20,decimal_places=2)
    # 对应股票
    stock = models.ForeignKey(StockTable, on_delete=models.CASCADE)

    def __str__(self):
        return '-'.join([self.stock_ts, self.stock_daily_date])

    class Meta:
        db_table = 'stock_daily_table'