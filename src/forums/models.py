from django.db import models
from django.utils import timezone
from PIL import Image

default_image = 'default.png'

class Forum(models.Model):
  name = models.CharField(max_length=100, unique=True)
  about = models.TextField()
  image = models.ImageField(default=default_image, upload_to='forum_pics')
  date_created = models.DateTimeField(default=timezone.now)
  owner = models.ForeignKey('users.profile', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
    
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
