from django.shortcuts import render

from news.models import NewsTable
from stock.models import StockTable
from tradingSystem.models import UserTable
# Create your views here.

def admin_index(request):
    return render(request, 'admin_index.html')

def admin_user(request):
    if request.method == 'GET':
        # 获取全部用户信息
        users = []  # 获取的评论内容
        users_data = UserTable.objects.all()
        for user_data in users_data:
            user = {}
            user['id'] = user_data.id
            user['name'] = user_data.user_name
            user['phone'] = user_data.phone_number
            user['email'] = user_data.user_email
            user['account_type'] = user_data.account_type
            user['account_num'] = user_data.account_num
            users.append(user)
        return render(request, 'admin_user.html', locals())

def admin_news(request):
    if request.method == 'GET':
        # 获取全部用户信息
        newses = []  # 获取的评论内容
        newses_data = NewsTable.objects.all()
        for news_data in newses_data:
            news = {}
            news['id'] = news_data.id
            news['title'] = news_data.news_title
            news['content'] = news_data.news_content
            news['src'] = news_data.news_src
            news['time'] = news_data.news_time
            newses.append(news)
        return render(request, 'admin_news.html', locals())

def admin_stock(request):
    if request.method == 'GET':
        # 获取全部用户信息
        stocks = []  # 获取的评论内容
        stocks_data = StockTable.objects.all()
        for stock_data in stocks_data:
            stock = {}
            stock['ts'] = stock_data.stock_ts
            stock['symbol'] = stock_data.stock_symbol
            stock['name'] = stock_data.stock_name
            stock['industry'] = stock_data.stock_industry
            stock['market'] = stock_data.stock_market
            stock['date'] = stock_data.stock_list_date
            stocks.append(stock)
        return render(request, 'admin_stock.html', locals())
