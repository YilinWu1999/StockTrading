"""StockTrading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tradingSystem import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', include('administer.urls')),
    # path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('index/', views.index, name='index'),
    path('user_detail/',views.user_detail, name='user_detail'),
    path('user_out/',views.user_out, name='user_out'),
    path('community/', include('community.urls')),
    path('stock/', include('stock.urls')),
    path('news/',include('news.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
