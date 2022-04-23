from django.urls import path, include

from news import views

urlpatterns = [
    path('all/',views.news_all, name='news_all'),

]