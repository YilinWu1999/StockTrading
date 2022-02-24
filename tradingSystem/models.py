from django.db import models

# Create your models here.


class UserTable(models.Model):
    # 用户信息表
    # 用户ID，
    user_id = models.CharField(max_length=12)
    # 身份证号码
    id_no = models.CharField(max_length=18)
    # 用户名，用于显示和评论
    user_name = models.CharField(max_length=45)
    # 用户密码
    password = models.CharField(max_length=45)
    # 用户性别
    user_sex = models.CharField(max_length=5)
    # 用户电话号码，用于注册，开户，联系，PK
    phone_number = models.CharField(max_length=45, primary_key=True)
    # 用户邮箱
    user_email = models.EmailField()
    # 用户头像路径
    photo_url = models.CharField(max_length=45)
    # 银行卡号
    account_num = models.CharField(max_length=45)
    # 银行卡类型
    account_type = models.CharField(max_length=45)
    # 账户余额
    account_balance = models.FloatField(null=True)
    # 是否冻结
    freeze = models.BooleanField(default=False)
    # 是否成功开户
    account_opened = models.BooleanField(default=True)
    # last_login
    last_login = models.CharField(max_length=45,null=True)

    def __str__(self):
        return '-'.join([self.user_name, self.phone_number])

    class Meta:
        db_table = 'user_table'