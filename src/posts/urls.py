from django.urls import path
from .views import PostList, PostDetail
from rest_framework import routers

urlpatterns = [
  path('', PostList.as_view(), name='post-list'),
  path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
