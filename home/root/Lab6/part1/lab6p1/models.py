# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here
class Label(models.Model):
        label_text = models.CharField(max_length=200)
        image_label = models.CharField(max_length=200)
