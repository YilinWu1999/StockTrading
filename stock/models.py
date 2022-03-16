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