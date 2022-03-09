from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.community_index, name='community_index'),
    path('add/', views.comment_add, name='comment_add')
]