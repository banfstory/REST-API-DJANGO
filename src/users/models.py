from django.db import models
from django.contrib.auth.models import User
from forums.models import Forum
from django.utils import timezone
from PIL import Image

default_image = 'default.png'

class Profile(models.Model):
  user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
  image = models.ImageField(default='default.png', upload_to='profile_pics')
  date_created = models.DateTimeField(default=timezone.now)
  follow_forums = models.ManyToManyField(Forum, through='Follower')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    super().save()
    img = Image.open(self.image.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)
  
  def set_image_default(self):
    self.image = default_image
    self.save()

class Follower(models.Model):
  date_followed = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.user.user.username} follows {self.forum.name}'

