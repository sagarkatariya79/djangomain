# Generated by Django 3.0 on 2022-01-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0002_signup'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='image',
            field=models.ImageField(default='', upload_to='user_images/'),
            preserve_default=False,
        ),
    ]