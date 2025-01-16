from django.db import models
from django.conf import settings

class Docs(models.Model):
    id = models.IntegerField
    file_path = models.CharField(max_length=100)
    size = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.id

class UsersToDocs(models.Model):
    id = models.IntegerField
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Price(models.Model):
    id = models.IntegerField
    file_type = models.CharField(max_length=10, blank=True)
    price = models.BigIntegerField(default=0)

    def __str__(self):
        return self.file_type

class Cart(models.Model):
    id = models.IntegerField
    user_id = models.ForeignKey(UsersToDocs, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)
    price_id = models.ForeignKey(Price, on_delete=models.CASCADE, default=0)
    order_price = models.FloatField(default=0, blank=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.id