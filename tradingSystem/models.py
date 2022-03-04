from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.


class UserTable(models.Model):
    # 用户信息表
    # 身份证号码
    id_no = models.CharField(max_length=18, unique=True)
    # 用户名，用于显示和评论
    user_name = models.CharField(max_length=45)
    # 用户密码
    password = models.CharField(max_length=45)
    # 用户电话号码，用于注册，开户，联系，PK
    phone_number = models.CharField(max_length=45, unique=True)
    # 用户邮箱
    user_email = models.EmailField(unique=True)
    # 用户头像路径
    photo_url = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                    # 图片将处理成100 x 100的尺寸
                                    processors=[ResizeToFill(160, 160)], )
    # 银行卡号
    account_num = models.CharField(max_length=45, null=True)
    # 银行卡类型
    account_type = models.CharField(max_length=45, null=True)
    # 账户余额
    account_balance = models.FloatField(null=True)
    # 是否冻结
    freeze = models.BooleanField(default=False)
    # 是否成功开户
    account_opened = models.BooleanField(default=True)
    # 最后登陆时间
    last_login = models.CharField(max_length=45, null=True)

    def __str__(self):
        return '-'.join([self.user_name, self.phone_number])

    class Meta:
        db_table = 'user_table'

class StockTable(models.Model):
    # 股票信息表，记录股票系统中的股票信息
    # 股票ts代码
    stock_ts =  models.CharField(max_length=10, primary_key=True)
    # 股票代码，固定6位，PK
    stock_symbol = models.CharField(max_length=6)
    # 股票名称
    stock_name = models.CharField(max_length=45)
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