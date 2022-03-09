from django.shortcuts import render, redirect
import time
from .models import *
# Create your views here.
def community_index(request):
    return render(request,'community_index.html')

def comment_add(request):
    if request.method == 'GET':
        return render(request, 'community_index.html')
    elif request.method == 'POST':
        #添加评论
        message = ''
        comment_title = request.POST['title']
        comment_content = request.POST['content']
        comment_user_id = request.session.get('uid')
        comment_stock_ts = request.POST['stock_ts']
        file_obj = request.FILES.get('photo_url')
        print(comment_user_id)
        print(comment_stock_ts)
        if file_obj:
            file_name = './media/comment/' + str(comment_user_id) + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[
                -1]  # 构造文件名以及文件路径
            photo_url = 'comment/' + str(comment_user_id) + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[-1]
            if file_obj.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
                message = '输入文件有误'
        if not message:
            try:
                print('11111')
                comment = CommentTable.objects.create(
                    comment_title = comment_title,
                    comment_content = comment_content,
                    comment_stock_id = comment_stock_ts,
                    comment_user_id = comment_user_id,
                )
                if file_obj:
                     comment.comment_photo = photo_url
                comment.save()
                if file_obj:
                    with open(file_name, 'wb+') as f:
                        f.write(file_obj.read())
            except Exception:
                print(Exception)
                message = "文章发布失败"
        print(message)
        request.session['message'] = message
        return redirect('community_index')