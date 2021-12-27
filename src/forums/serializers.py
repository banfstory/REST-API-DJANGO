from rest_framework import serializers
from .models import Forum
from users.models import Profile

class ForumSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
  date_created = serializers.ReadOnlyField()
  post_count = serializers.IntegerField(source='post_set.count',read_only=True)
  follower_count = serializers.IntegerField(source='follower_set.count',read_only=True)

  class Meta:
    model = Forum
    fields = ('url' ,'id', 'name', 'about', 'image', 'post_count', 'follower_count', 'date_created', 'owner')
    read_only_fields = ['id', 'date_created', 'owner']
  
  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    # if the method been used is PUT than make name read only
    if request.method == 'GET':
      fields['owner'] = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
    elif request.method == 'PUT': 
      fields['owner'].read_only = True
    return fields