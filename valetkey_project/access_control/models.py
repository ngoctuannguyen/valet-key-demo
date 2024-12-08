import base64
import datetime
import hashlib
import hmac
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
import urllib.parse

# Resource Model
class Resource(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resource uploaded by {self.uploader}'

# Valet Key Model
class ValetKey(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)
    key = models.TextField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    active = models.BooleanField(default=True)

    def is_valid(self):
        return self.active and timezone.now() < self.expires_at

    def deactivate(self):
        self.active = True
        self.save()

    def __str__(self):
        return f'ValetKey for {self.user} valid until {self.expires_at}'

