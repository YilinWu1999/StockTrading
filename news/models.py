from django.db import models

# Create your models here.
class NewsTable(models.Model):
    # 新闻标题
    news_title = models.CharField(max_length=100)
    # 新闻内容
    news_content = models.TextField()
    # 新闻发布时间
    news_time = models.DateTimeField(auto_now=True)
    # 新闻来源
    news_src = models.CharField(max_length=100)

    def __str__(self):
        return '-'.join([str(self.id), self.news_title])

    class Meta:
        db_table = 'news_table'
        ordering = ['-news_time']