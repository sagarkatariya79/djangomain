# Generated by Django 3.0 on 2022-01-31 16:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0006_products_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eapp.Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eapp.Signup')),
            ],
        ),
    ]
