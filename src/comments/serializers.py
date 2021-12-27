from rest_framework import serializers
from .models import Comment
from users.models import Profile
from posts.models import Post

class CommentSerializer(serializers.HyperlinkedModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
  post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
  reply_count = serializers.IntegerField(source='reply_set.count', read_only=True)

  class Meta:
    model = Comment
    fields = ('url', 'id', 'content', 'reply_count', 'date_commented', 'user', 'post')
    read_only_fields = ['id', 'date_commented']

  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    if request.method == 'GET':
      fields['user'] = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
      fields['post'] = serializers.HyperlinkedRelatedField(many=False, view_name='post-detail', read_only=True)
    # if the method been used is PUT than make name read only
    if request and request.method == 'PUT': 
      fields['user'].read_only = True
      fields['post'].read_only = True
    return fields
  