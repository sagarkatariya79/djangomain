# Generated by Django 3.0 on 2022-02-11 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0009_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='address',
            field=models.TextField(default='India'),
        ),
    ]
