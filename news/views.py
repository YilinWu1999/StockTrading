from django.shortcuts import render
from news.models import NewsTable
import tushare as ts
from datetime import date, timedelta
import time
# Create your views here.



def news_get(num):
    ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
    pro = ts.pro_api()
    # 获取时间
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    hms = time.strftime(" %H:%M:%S", time.localtime())
    # 获取新闻数据
    try:
        news_data = pro.major_news(src='', start_date=yesterday+hms, end_date=today+hms,
                            fields='title,content,pub_time,src')
        for i in range(0, len(news_data)):
            news_title = news_data.loc[i, 'title']
            news_content = news_data.loc[i, 'content']
            news_time = news_data.loc[i, 'pub_time']
            news_src = news_data.loc[i, 'src']
            if not NewsTable.objects.filter(news_title=news_title):
                break
            try:
                news = NewsTable.objects.create(
                    news_title = news_title,
                    news_content = news_content,
                    news_time = news_time,
                    news_src = news_src
                )
                news.save()
            except Exception:
                print(Exception)
    except Exception as e:
        print(e)
    news_all = NewsTable.objects.all()

    if num == 0 :
        num = len(news_all)
    newses = []
    for news_data in news_all[0:num]:
        news = {}
        news['title'] = news_data.news_title
        news['content'] = news_data.news_content
        news['src'] = news_data.news_src
        news['time'] = news_data.news_time
        newses.append(news)
    return newses