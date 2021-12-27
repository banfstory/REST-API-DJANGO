from django.db import models
from django.utils import timezone
from users.models import Profile
from comments.models import Comment

class Reply(models.Model):
  content = models.TextField()
  date_replied = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)