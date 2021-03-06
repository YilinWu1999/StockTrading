from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('index/', views.community_index, name='community_index'),
    path('add/', views.comment_add, name='comment_add'),
    path('del/', views.comment_del, name='comment_del'),
    path('discuss_add', views.dicuss_add, name='discuss_add'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件