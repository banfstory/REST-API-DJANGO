from rest_framework import serializers
from .models import Post
from users.models import Profile
from forums.models import Forum

class PostSerializer(serializers.HyperlinkedModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
  forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
  comment_count = serializers.IntegerField(source='comment_set.count',read_only=True)

  class Meta:
    model = Post
    fields = ('url', 'id', 'title', 'content', 'comment_count', 'date_posted', 'user', 'forum')
    read_only_fields = ['id', 'date_posted']

  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    if request.method == 'GET':
      fields['user'] = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
      fields['forum'] = serializers.HyperlinkedRelatedField(many=False, view_name='forum-detail', read_only=True)
    # if the method been used is PUT than make name read only
    elif request.method == 'PUT': 
      fields['user'].read_only = True
      fields['forum'].read_only = True
    return fields