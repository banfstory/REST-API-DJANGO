from django.db import models
from django.utils import timezone
from users.models import Profile
from forums.models import Forum
from django.urls import reverse

class Post(models.Model):
  title = models.CharField(max_length=200)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
