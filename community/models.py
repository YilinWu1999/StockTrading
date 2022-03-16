from django.db import models

from stock.models import StockTable
from tradingSystem.models import *
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

class CommentTable(models.Model):
    # 评论标题
    comment_title = models.CharField(max_length=100)
    # 评论内容
    comment_content = models.TextField()
    # 评论发布用户
    comment_user = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    # 评论相关股票
    comment_stock = models.ForeignKey(StockTable, on_delete=models.CASCADE, null=True)
    # 评论
    comment_time = models.DateTimeField(auto_now=True)
    # 评论附加图片
    comment_photo = ProcessedImageField(upload_to='comment', verbose_name='评论图片',
                                        # 图片将处理成100 x 100的尺寸
                                        processors=[ResizeToFill(160, 160)], null=True)

    def __str__(self):
        return '-'.join([str(self.id), self.comment_title])

    class Meta:
        db_table = 'comment_table'
        ordering = ['-comment_time']

class DiscussTable(models.Model):
    # 评论评论的内容
    discuss_content = models.CharField(max_length=100)
    # 评论的时间
    discuss_time = models.DateTimeField(auto_now=True)
    # 评论的对象
    discuss_to = models.ForeignKey(CommentTable, on_delete=models.CASCADE)
    # 评论用户
    discuss_user = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    def __str__(self):
        return '-'.join([str(self.id), self.discuss_user])

    class Meta:
        db_table = 'discuss_table'
        ordering = ['-discuss_time']
