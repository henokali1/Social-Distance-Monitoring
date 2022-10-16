from django.db import models
from time import time
from django.utils import timezone

from django.db.models.fields import DateTimeField


# Report
class Report(models.Model):
    img_url = models.CharField(default="", max_length=255)
    date = DateTimeField(default=timezone.now)
    ts = models.IntegerField(default=int(time()))

    def __str__(self):
        r = f'Date: {self.date} ts: {self.ts} - img_url: {self.img_url}'
        return r

# Jetson Nano IP Address
class Ip(models.Model):
    ip = models.CharField(default="", max_length=255)
    raw = models.CharField(default="", max_length=255)
    ts = models.IntegerField(default=int(time()))
    def __str__(self):
        r = f'IP - {self.ip}'
        return r
