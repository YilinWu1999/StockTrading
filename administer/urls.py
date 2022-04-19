from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('index/', views.admin_index, name='admin_index'),
    path('user/', views.admin_user, name='admin_user'),
    path('news/', views.admin_news, name='admin_news'),
    path('stock/', views.admin_stock, name='admin_stock'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件