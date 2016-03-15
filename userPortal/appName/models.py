from datetime import datetime
from django.db import models

# Create your models here.
class Opcache(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(u'user', max_length=64)
    category = models.CharField(u'category', max_length=64)
    params = models.CharField(u'params', max_length=1024)
    updatetime = models.DateTimeField(default=datetime.now(), blank=True)
    content = models.TextField(u'content')

    def __unicode__(self):
        return self.user

