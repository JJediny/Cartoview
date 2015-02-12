from django.db import models
from django.contrib.sites.models import Site

# Create your models here.
class Settings(models.Model):
    site = models.OneToOneField(Site , related_name='registeration_settings')
    enable_social = models.BooleanField(default=True)
