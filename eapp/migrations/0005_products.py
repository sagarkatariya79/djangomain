# Generated by Django 3.0 on 2022-01-19 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0004_signup_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category', models.CharField(choices=[('Leptop', 'Leptop'), ('Mobile', 'Mobile'), ('Camera', 'Camera')], max_length=100)),
                ('product_company', models.CharField(choices=[('Dell', 'Dell'), ('Lenovo', 'Lenovo'), ('Hp', 'Hp'), ('Xaiomi', 'Xaiomi'), ('Samsung', 'Samsung'), ('Vivo', 'Vivo'), ('Canon', 'Canon'), ('Nikon', 'Nikon'), ('Fujifilm', 'Fujifilm')], max_length=100)),
                ('product_desc', models.TextField()),
                ('product_price', models.PositiveIntegerField()),
                ('product_image', models.ImageField(upload_to='product_image/')),
                ('product_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eapp.Signup')),
            ],
        ),
    ]
