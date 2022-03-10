from django.shortcuts import render, redirect
import time
from .models import *
# Create your views here.
def community_index(request):
    if request.method == 'GET':
        # 1.获取全部评论
        comment_num = 0 #评论数量
        comments = [] #获取的评论内容
        comments_data = CommentTable.objects.all()
        for comment_data in comments_data:
            comment = {}
            comment['comment_title'] = comment_data.comment_title
            comment['comment_content'] = comment_data.comment_content
            comment['comment_photo'] = comment_data.comment_photo
            comment['user_name'] = comment_data.comment_user.user_name
            comment['user_avatar'] = comment_data.comment_user.photo_url
            comment['comment_time'] = comment_data.comment_time
            comment['stock_ts'] = comment_data.comment_stock.stock_ts
            comments.append(comment)
            comment_num+=1
        # 2.获取当前用户的评论
        return render(request, 'community_index.html', locals())

    elif request.method == 'POST':
        # 评论当前评论
        return render(request, 'community_index.html')

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
        if file_obj:
            file_name = './media/comment/' + str(comment_user_id) + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[
                -1]  # 构造文件名以及文件路径
            photo_url = 'comment/' + str(comment_user_id) + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[-1]
            if file_obj.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
                message = '输入文件有误'
        if not message:
            try:
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