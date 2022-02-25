from django.shortcuts import render
from .models import *


# Create your views here.

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = UserTable.objects.get(phone_number=phone_number)
        if (user.password == password):
            return render(request, 'index.html')
        else:
            return render(request, 'login.html')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        user_sex = request.POST['user_sex']
        id_no = request.POST['id_no']
        user_email = request.POST['user_email']
        password = request.POST['password']
        account_type = request.POST['account_type']
        account_number = request.POST['account_number']
        message = ""
        try:
            user = UserTable.objects.create(
                user_id=1,
                user_name=user_name,
                user_email=user_email,
                user_sex=user_sex,
                id_no=id_no,
                password=password,
                account_type=account_type,
                account_num=account_number,
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
        return render(request,'register.html')
