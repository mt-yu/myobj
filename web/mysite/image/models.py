from django.db import models
from django.contrib.auth.models import User
from slugify import slugify  # slug 用于将中文转成拼音 空格转成'-'
import uuid
import os


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(instance.user.id, "image", filename)


class Image(models.Model):
    user = models.ForeignKey(User, related_name="images", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    url = models.URLField()
    slug = models.SlugField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    url_height = models.PositiveIntegerField(default=75)
    url_width = models.PositiveIntegerField(default=75)
    # image = models.ImageField(upload_to='images/%Y/%m/%d')
    image = models.ImageField(upload_to='images/%Y/%m/%d',
                              height_field='url_height', width_field='url_width')
    # image = models.FileField(upload_to='images/%Y/%m/%d')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
