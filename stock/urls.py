from django.urls import path, include

from stock import views

urlpatterns = [
    path('update/',views.stock_update, name='stock_update'),
    path('all/', views.stock_all, name='stock_all'),
]