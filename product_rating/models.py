from django.db import models
from django.conf import settings

class Product_Table(models.Model):
    product_name = models.CharField(max_length=255, blank=False)
    product_description = models.CharField(max_length=1000, blank=False)
    product_ratings = models.IntegerField(default=0)
    ratings_sum = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    ratings_average = models.FloatField(default=0)
    product_quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{}".format(self.name)

class Product_User_Table(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user")
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255, blank=False)
    product_ratings = models.IntegerField(default=0)
    product_quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.product_name).format(self.product_ratings).format(self.product_quantity)
