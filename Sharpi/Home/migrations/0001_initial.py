# Generated by Django 4.2.10 on 2024-03-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tokens_alredy_have',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=20)),
                ('is_details', models.IntegerField()),
            ],
        ),
    ]
