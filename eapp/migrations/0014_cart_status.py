# Generated by Django 3.0 on 2022-02-12 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0013_auto_20220212_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
