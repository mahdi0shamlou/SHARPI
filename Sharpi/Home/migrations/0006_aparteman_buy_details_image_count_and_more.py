# Generated by Django 4.2.10 on 2024-03-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_aparteman_buy_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparteman_buy_details',
            name='image_count',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='aparteman_buy_details',
            name='price',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='aparteman_buy_details',
            name='rent',
            field=models.CharField(default=None, max_length=255),
        ),
    ]