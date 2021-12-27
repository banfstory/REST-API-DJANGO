from .serializers import ForumSerializer
from rest_framework import generics
from custom_errors.errors import profileError, unauthorized_access_error
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Forum


class ForumList(generics.ListCreateAPIView):
  queryset = Forum.objects.all()
  serializer_class = ForumSerializer

  def get_queryset(self):
    q = self.request.query_params.get('q', None)
    name = self.request.query_params.get('name', None)
    owner_id = self.request.query_params.get('owner', None)
    param = {}
    if q is not None:
      param['name__icontains'] = q
    if name is not None:
      param['name__iexact'] = name
    if owner_id is not None:
      param['owner'] = owner_id
    return Forum.objects.filter(**param)
  
  def post(self, request):
    profile = request.user.profile
    if profile is None:
      return profileError()
    name = request.data.get('name', None)
    if name and forum_exist(name):
      return forum_error()
    request.data['owner'] = profile.id
    return super().post(request)

class ForumDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Forum.objects.all()
  serializer_class = ForumSerializer  

  def put(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    forum = get_object_or_404(Forum, pk=pk)
    if profile.id != forum.owner.id:
      return unauthorized_access_error()
    name = request.data.get('name', None)
    if name and name != forum.name and forum_exist(name):
      return forum_error()
    return super().put(request, pk)

  def delete(self, request, pk):
    profile = request.user.profile
    if profile is None:
      return profileError
    forum = get_object_or_404(Forum, pk=pk)
    if profile.id != forum.owner.id:
      return unauthorized_access_error()
    return super().delete(request, pk)

@api_view(['PUT'])
def forum_image_default(request, pk):
  if request.method == 'PUT':
    profile = request.user.profile
    if profile is None:
      return profileError
    forum = get_object_or_404(Forum, pk=pk)
    if profile.id != forum.owner.id:
      return unauthorized_access_error()
    forum.set_image_default()
    return Response({'message': 'User image set to default'}, status=status.HTTP_200_OK)

# check if forum name already exist
def forum_exist(name):
  forum = Forum.objects.filter(name__iexact=name).first()
  return forum

# forum error message as it already exist
def forum_error():
  return Response({'message' : 'Forum name already exist'}, status=status.HTTP_400_BAD_REQUEST)