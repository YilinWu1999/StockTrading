from django.db import models
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
    comment_user_id = models.ForeignKey(to=UserTable, on_delete=models.CASCADE)
    # 评论相关股票
    comment_stock_ts = models.ForeignKey(to=StockTable, on_delete=models.CASCADE, null=True)
    # 评论
    comment_time = models.DateField(auto_now=True)
    # 评论附加图片
    comment_photo = ProcessedImageField(upload_to='comment', verbose_name='评论图片',
                                        # 图片将处理成100 x 100的尺寸
                                        processors=[ResizeToFill(160, 160)], null=True)

    def __str__(self):
        return '-'.join([str(self.id), self.comment_title])

    class Meta:
        db_table = 'comment_table'
        ordering = ['comment_time']
