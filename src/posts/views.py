from .serializers import PostSerializer
from rest_framework import generics
from custom_errors.errors import profileError, unauthorized_access_error
from django.shortcuts import get_object_or_404
from .models import Post

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

  def get_queryset(self):
    forum_id = self.request.query_params.get('forum', None)
    user_id = self.request.query_params.get('user', None)
    param = {}
    if forum_id is not None:
      param['forum'] = forum_id
    if user_id is not None:
      param['user'] = user_id
    return Post.objects.filter(**param)
  
  def post(self, request):
    profile = request.user.profile
    if profile is None:
      return profileError()
    request.data['user'] = profile.id
    return super().post(request)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

  def put(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    post = get_object_or_404(Post, pk=pk)
    if post and profile.id != post.user.id:
      return unauthorized_access_error()
    return super().put(request, pk)

  def delete(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    post = get_object_or_404(Post, pk=pk)
    if post and profile.id != post.user.id:
      return unauthorized_access_error()
    return super().delete(request, pk)