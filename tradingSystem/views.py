from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
import tushare as ts


# Create your views here.

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
        request.session['photo_url'] = str(user.photo_url)
        return redirect('index')


def user_out(request):
    if request.method == 'GET':
        request.session.flush()
        return redirect('index')
    elif request.method == 'POST':
        return redirect('index')


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
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        id_no = request.POST['id_no']
        user_email = request.POST['user_email']
        password = request.POST['password']
        ensure_password = request.POST['ensure_password']
        account_type = request.POST['account_type']
        account_num = request.POST['account_num']
        photo_url = request.FILES.get('')
        message = ''
        if ensure_password != password:
            message = "确认密码不符"
        else:
            try:
                user = UserTable.objects.get(phone_number=phone_number)
                user.phone_number = phone_number
                user.user_name = user_name
                user.user_email = user_email
                user.password = password
                user.account_type = account_type
                user.account_num = account_num
                user.id_no = id_no
                user.save()
            except Exception:
                message = "修改信息失败，请仔细检查，或稍后重试"
        request.session['username'] = user_name
        request.session['message'] = message
        return redirect('user_detail')


def index(request):
    if request.method == 'GET':
        # 处理登陆状态
        uid = request.session.get('uid')
        if uid:
            user = UserTable.objects.get(id=uid)
            user_name = user.user_name
            request.session['username'] = user_name

        #获取股票数据
        stocks = []
        ts.set_token('e4ef519ae1e2dcc00beb8d11707219e6274cf24c77668e95ffd63774')
        pro = ts.pro_api()
        # 查询当前所有正常上市交易的股票列表
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        for i in range(0,10):
            stock = {}
            stock['symbol'] = data.loc[i,'symbol']
            stock['name'] = data.loc[i,'name']
            stocks.append(stock)
        return render(request, 'index.html', locals())
    elif request.method == 'POST':
        return render(request, 'index.html')
