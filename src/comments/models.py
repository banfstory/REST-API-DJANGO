from django.db import models
from django.utils import timezone
from users.models import Profile
from posts.models import Post

class Comment(models.Model):
  content = models.TextField()
  date_commented = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
