from .serializers import CommentSerializer
from rest_framework import generics
from custom_errors.errors import profileError, unauthorized_access_error
from django.shortcuts import get_object_or_404
from .models import Comment

class CommentList(generics.ListCreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

  def get_queryset(self):
    post_id = self.request.query_params.get('post', None)
    user_id = self.request.query_params.get('user', None)
    param = {}
    if post_id is not None:
      param['post'] = post_id
    if user_id is not None:
      param['user'] = user_id
    return Comment.objects.filter(**param)
  
  def post(self, request):
    profile = request.user.profile
    if profile is None:
      return profileError()
    request.data['user'] = profile.id
    return super().post(request)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

  def put(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    comment = get_object_or_404(Comment, pk=pk)
    if profile.id != comment.user.id:
      return unauthorized_access_error()
    return super().put(request, pk)

  def delete(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    comment = get_object_or_404(Comment, pk=pk)
    if profile.id != comment.user.id:
      return unauthorized_access_error()
    return super().delete(request, pk)