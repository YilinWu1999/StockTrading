from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.


class AdminUserTable(models.Model):
    # 管理员信息表
    # 管理员名
    admin_name = models.CharField(max_length=45)
    # 管理员密码
    admin_password = models.CharField(max_length=45)
    # 管理员电话号码
    admin_phone = models.CharField(max_length=45, unique=True)
    # 管理员邮箱
    admin_email = models.EmailField(unique=True)
    # 管理员头像路径
    admin_photo_url = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                    # 图片将处理成100 x 100的尺寸
                                    processors=[ResizeToFill(160, 160)], )

    def __str__(self):
        return '-'.join([self.admin_name, self.admin_phone])

    class Meta:
        db_table = 'admin_user_table'
