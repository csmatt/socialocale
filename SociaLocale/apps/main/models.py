from django.db import models

class SubscribeEmail(models.Model):
    email = models.EmailField()