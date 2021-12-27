from .serializers import ReplySerializer
from rest_framework import generics
from custom_errors.errors import profileError, unauthorized_access_error
from django.shortcuts import get_object_or_404
from .models import Reply

class ReplyList(generics.ListCreateAPIView):
  queryset = Reply.objects.all()
  serializer_class = ReplySerializer

  def get_queryset(self):
    comment_id = self.request.query_params.get('comment', None)
    user_id = self.request.query_params.get('user', None)
    param = {}
    if comment_id is not None:
      param['comment'] = comment_id
    if user_id is not None:
      param['user'] = user_id
    return Reply.objects.filter(**param)
  
  def post(self, request):
    profile = request.user.profile
    if profile is None:
      return profileError()
    request.data['user'] = profile.id
    return super().post(request)

class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Reply.objects.all()
  serializer_class = ReplySerializer

  def put(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    reply = get_object_or_404(Reply, pk=pk)
    if profile.id != reply.user.id:
      return unauthorized_access_error()
    return super().put(request, pk)

  def delete(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    reply = get_object_or_404(Reply, pk=pk)
    if profile.id != reply.user.id:
      return unauthorized_access_error()
    return super().delete(request, pk)