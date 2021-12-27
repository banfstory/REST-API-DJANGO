from rest_framework import serializers
from .models import Reply
from users.models import Profile
from comments.models import Comment

class ReplySerializer(serializers.HyperlinkedModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
  comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

  class Meta:
    model = Reply
    fields = ('url', 'id', 'content', 'date_replied', 'user', 'comment')
    read_only_fields = ['id', 'date_replied']

  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    if request.method == 'GET':
      fields['user'] = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
      fields['comment'] = serializers.HyperlinkedRelatedField(many=False, view_name='comment-detail', read_only=True)
    # if the method been used is PUT than make name read only
    if request and request.method == 'PUT': 
      fields['user'].read_only = True
      fields['comment'].read_only = True
    return fields