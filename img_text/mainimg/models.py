from django.db import models
from django.conf import settings

class Docs(models.Model):
    id = models.IntegerField
    file_path = models.CharField(max_length=100)
    size = models.IntegerField(blank=True, default=0)

class UsersToDocs(models.Model):
    id = models.IntegerField
    username = models.CharField(max_length=50)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)

class Price(models.Model):
    id = models.IntegerField
    file_type = models.CharField(max_length=10, blank=True)
    price = models.BigIntegerField(default=0)

class Cart(models.Model):
    id = models.IntegerField
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)
    order_price = models.FloatField(default=0)
    payment = models.BooleanField