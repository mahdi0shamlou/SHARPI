from django.db import models

class Tokens_alredy_have(models.Model):
  id = models.IntegerField(primary_key=True, auto_created=True)
  token = models.CharField(max_length=20)
  is_details = models.IntegerField()
  class Meta:
    db_table = 'Tokens_alredy_have'
class Aparteman_buy_details(models.Model):
  id = models.IntegerField(primary_key=True, auto_created=True)
  token = models.CharField(max_length=20)
  mahal_english = models.CharField(max_length=255)
  image_count = models.IntegerField(default=None)
  rent = models.CharField(max_length=255, default=None)
  price = models.BigIntegerField(default=None)
  city = models.CharField(max_length=255, default=None)
  #title = models.CharField(max_length=255, default=None)
  city_persian = models.CharField(max_length=255, default=None)
  mahal_persian = models.CharField(max_length=255, default=None)
  class Meta:
    db_table = 'Aparteman_buy_details'
# Create your models here.
