from urllib import request

from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')
    title = models.TextField(null=True)
    desc = models.TextField(null=True)
    columns = models.JSONField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
