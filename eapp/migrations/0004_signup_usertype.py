# Generated by Django 3.0 on 2022-01-17 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0003_signup_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='usertype',
            field=models.CharField(default='user', max_length=100),
        ),
    ]
