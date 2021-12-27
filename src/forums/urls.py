from django.urls import path, include
from .views import ForumList, ForumDetail, forum_image_default
urlpatterns = [
  path('', ForumList.as_view(), name='forum-list'),
  path('<int:pk>/', ForumDetail.as_view(), name='forum-detail'),
  path('<int:pk>/default-image/', forum_image_default, name='forum-default-image'),
]
