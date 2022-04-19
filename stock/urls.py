from django.urls import path, include

from stock import views

urlpatterns = [
    path('update/',views.stock_update, name='stock_update'),
    path('all/', views.stock_all, name='stock_all'),
    path('detail/', views.stock_detail, name='stock_detail'),
    path('optional/', views.stock_optional, name='stock_opyional'),
    path('optional/add', views.stock_optional_add, name='stock_optional_add'),
    path('optional/del', views.stock_optional_del, name='stock_optional_del'),
    path('detail/daily_kline/', views.daily_kline, name="daily_kline"),
    path('detail/week_kline/', views.week_kline, name="week_kline"),
    path('detail/month_kline/', views.month_kline, name="month_kline")
]