from django.urls import path, include
from .views import  ProfileList, ProfileDetail, FollowerList, FollowerDetail, user_image_default

urlpatterns = [
  path('', ProfileList.as_view(), name='profile-list'),
  path('<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
  path('followers/', FollowerList.as_view(), name='follower-list'),
  path('<int:pk>/followers/', FollowerDetail.as_view(), name='follower-detail'),
  path('default-image/', user_image_default, name='user-default-image'),
]
