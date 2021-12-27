from .serializers import ProfileSerializer, FollowerSerializer
from rest_framework import generics, permissions
from custom_errors.errors import profileError, unauthorized_access_error
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Profile, Follower

# create base permission to allow 'GET' and 'POST' by default but only allow 'PUT' if user is authenticated
class IsReadPostOrIsAuthenticated(permissions.BasePermission):
  def has_permission(self, request, view):
    if  request.method == 'GET' or request.method == 'POST':
        return True
    return request.user and request.user.is_authenticated

class ProfileList(generics.ListCreateAPIView):
  permission_classes = (IsReadPostOrIsAuthenticated,)
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def get_queryset(self):
    q = self.request.query_params.get('q', None)
    username = self.request.query_params.get('username', None)
    param = {}
    if q is not None:
      param['user__username__icontains'] = q
    if username is not None:
      param['user__username__iexact'] = username
    return Profile.objects.filter(**param)

  def post(self, request):
    username = request.data.get('username', None)
    if username and user_exist(username):
      return user_error()
    return super().post(request)

class ProfileDetail(generics.RetrieveUpdateAPIView):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def put(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    user = get_object_or_404(Profile, pk=pk)
    if profile.id != user.id:
      return unauthorized_access_error()
    username = request.data.get('username', None)
    if username and username != request.user.username and user_exist(username):
      return user_error()
    return super().put(request, pk)

class FollowerList(generics.ListCreateAPIView):
  queryset = Follower.objects.all()
  serializer_class = FollowerSerializer

  def get_queryset(self):
    user_id = self.request.query_params.get('user', None)
    forum_id = self.request.query_params.get('forum', None)
    param = {}
    if user_id is not None:
      param['user'] = user_id
    if forum_id is not None:
      param['forum'] = forum_id
    return Follower.objects.filter(**param)

  def post(self, request):
    profile = request.user.profile
    if profile is None:
      return profileError
    forum_id = request.data.get('forum', None)
    if follower_exist(profile, forum_id):
      return follower_error()
    request.data['user'] = profile.id
    return super().post(request)

class FollowerDetail(generics.RetrieveDestroyAPIView):
  queryset = Follower.objects.all()
  serializer_class = FollowerSerializer

  def delete(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    follower = get_object_or_404(Follower, pk=pk)
    if profile.id != follower.user.id:
      return unauthorized_access_error()
    return super().delete(request, pk)

@api_view(['PUT'])
def user_image_default(request):
  if request.method == 'PUT':
    profile = request.user.profile
    if profile is None:
      return profileError
    profile.set_image_default()
    return Response({'message': 'User image set to default'}, status=status.HTTP_200_OK)

# check if user name already exist
def user_exist(name):
  user = Profile.objects.filter(user__username__iexact=name).first()
  return user

# user error message as it already exist
def user_error():
  return Response({'message' : 'User name already exist'}, status=status.HTTP_400_BAD_REQUEST)

# check if user is already following this forum
def follower_exist(profile, forum_id):
  follower = profile.follow_forums.filter(id=forum_id)
  return follower

# follower error message as user is already following
def follower_error():
  return Response({'message' : 'User has already followed this forum'}, status=status.HTTP_400_BAD_REQUEST)