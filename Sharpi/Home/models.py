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
  class Meta:
    db_table = 'Aparteman_buy_details'
# Create your models here.
