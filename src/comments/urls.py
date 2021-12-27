from django.urls import path
from .views import CommentList, CommentDetail
from rest_framework import routers

urlpatterns = [
  path('', CommentList.as_view(), name='comment-list'),
  path('<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]
