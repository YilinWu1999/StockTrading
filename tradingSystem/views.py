from django.shortcuts import render, redirect
from django.db.models import Q

from stock.models import StockTable
from stock.views import stock_top
from .models import *
import tushare as ts
import time
from datetime import date, timedelta
from news.views import news_get


# Create your views here.

# 用户登陆
def user_login(request):
    if request.method == 'GET':
        if request.session.get('uid'):
            return render(request, 'index.html')
        c_uid = request.COOKIES.get('uid')
        if c_uid:
            request.session['uid'] = c_uid
            return render(request, 'index.html')
        return render(request, 'login.html')
    elif request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        message = ''
        try:
            user = UserTable.objects.get(phone_number=phone_number)
        except Exception as e:
            print('--login user error %s' % (e))
            message = '用户名或者密码错误'
            return render(request, 'login.html', locals())
        if user.password != password:
            message = '用户名或者密码错误'
            return render(request, 'login.html', locals())
        request.session['uid'] = user.id
        request.session['photo_url'] = user.photo_url.url
        return redirect('index')

# 用户退出
def user_out(request):
    if request.method == 'GET':
        request.session.flush()
        return redirect('index')
    elif request.method == 'POST':
        return redirect('index')

# 用户注册
def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        id_no = request.POST['id_no']
        user_email = request.POST['user_email']
        password = request.POST['password']
        ensure_password = request.POST['ensure_password']
        message = ""
        old_users = UserTable.objects.filter(Q(phone_number=phone_number) | Q(id_no=id_no) | Q(user_email=user_email))
        if password != ensure_password:
            message = "输入的两次密码不一致！"
            return render(request, 'register.html', locals())
        elif old_users:
            message = "手机号、邮箱或者身份证号已被注册"
            return render(request, 'register.html', locals())
        try:
            user = UserTable.objects.create(
                user_name=user_name,
                user_email=user_email,
                id_no=id_no,
                password=password,
                phone_number=phone_number,
                account_balance=0,
            )
            user.save()
            print("success register user")
            print(user)
        except Exception:
            print(Exception)
            message = "注册失败，请检查或稍后再试！"
            return render(request, 'register.html', locals())
        return render(request, 'login.html')

# 用户详细信息
def user_detail(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        if uid:
            user = UserTable.objects.get(id=uid)
            message = request.session.get('message')
            print(message)
            return render(request, 'user_detail.html', locals())
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        message = ''
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        id_no = request.POST['id_no']
        user_email = request.POST['user_email']
        password = request.POST['password']
        ensure_password = request.POST['ensure_password']
        account_type = request.POST['account_type']
        account_num = request.POST['account_num']
        file_obj = request.FILES.get('photo_url')
        # print(username,password,phone,e_mail)
        if file_obj:
            file_name = './media/avatar/' + user_name + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[
                -1]  # 构造文件名以及文件路径
            photo_url = 'avatar/' + user_name + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[-1]
            if file_obj.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
                message = '输入文件有误'
        if ensure_password != password:
            message = "确认密码不符"
        if not message:
            try:
                user = UserTable.objects.get(phone_number=phone_number)
                user.phone_number = phone_number
                user.user_name = user_name
                user.user_email = user_email
                user.password = password
                user.account_type = account_type
                user.account_num = account_num
                user.id_no = id_no
                if file_obj:
                    user.photo_url = photo_url
                user.save()
                if file_obj:
                    with open(file_name, 'wb+') as f:
                        f.write(file_obj.read())
            except Exception:
                message = "修改信息失败，请仔细检查，或稍后重试"
        request.session['message'] = message
        if not message:
            request.session['username'] = user_name
            request.session['photo_url'] = user.photo_url.url
        return redirect('user_detail')

# 网站首页
def index(request):
    if request.method == 'GET':
        # 处理登陆状态
        uid = request.session.get('uid')
        if uid:
            user = UserTable.objects.get(id=uid)
            user_name = user.user_name
            request.session['username'] = user_name

        # 获取龙虎榜股票数据
        stocks = []
        stocks = stock_top(10)

        # 获取今日新闻信息
        newses = []
        newses = news_get(10)

        return render(request, 'index.html', locals())
    elif request.method == 'POST':
        return render(request, 'index.html')

