from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follower
from forums.models import Forum
from django.contrib.auth.hashers import make_password, check_password

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
  username = serializers.CharField(source='user.username')
  email = serializers.CharField(source='user.email')
  password = serializers.CharField(source='user.password', write_only=True)
  follow_forums = serializers.HyperlinkedRelatedField(many=True, view_name='forum-detail', read_only=True)
  follower_count = serializers.IntegerField(source='follower_set.count',read_only=True)

  class Meta:
    model = Profile
    fields = ('url', 'id', 'username', 'email', 'password', 'follower_count', 'date_created', 'image', 'follow_forums')
    read_only_fields = ['id', 'date_created', 'follow_forums']

  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    # if the method been used is PUT than make name read only
    if request.method == 'PUT': 
      fields['password'].read_only = True
    return fields

  def create(self, validated_data):
    username = validated_data['user'].get('username')
    email = validated_data['user'].get('email')
    password = validated_data['user'].get('password')
    hashed_password = make_password(password)
    user = User(username=username, email=email, password=hashed_password)
    user.save()
    profile = Profile(user=user)
    profile.save()
    return profile

  def update(self, instance, validated_data):
    instance.user.username = validated_data['user'].get('username', instance.user.username)
    instance.user.email = validated_data['user'].get('email', instance.user.email)
    instance.image = validated_data.get('image', instance.image)
    instance.save()
    instance.user.save()
    return instance

class FollowerSerializer(serializers.HyperlinkedModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
  forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())

  class Meta:
    model = Follower
    fields = ('url', 'id', 'date_followed', 'user', 'forum')
    read_only_fields = ['id', 'date_followed']
  
  def get_fields(self):
    fields = super().get_fields()
    request = self.context.get('request', None) # to get the request object to access the method
    if request.method == 'GET':
      fields['user'] = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
      fields['forum'] = serializers.HyperlinkedRelatedField(many=False, view_name='forum-detail', read_only=True)
    return fields
