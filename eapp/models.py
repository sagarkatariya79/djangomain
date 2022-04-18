from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class Contact(models.Model):
    name=models.TextField(max_length='100')
    email=models.EmailField()
    message=models.TextField()

    # def __str__(self):
    #     return self.name


class User(models.Model):
    fname= models.CharField(max_length=100)
    lname= models.CharField(max_length=100)
    email= models.EmailField()
    mobile=models.PositiveIntegerField()
    address=models.TextField(default='India')
    password=models.CharField(max_length=20)
    image = models.ImageField(upload_to='user_images/')
    usertype =models.CharField(max_length=100,default='user')
    
    def __str__(self):
        return self.fname


class Products(models.Model):
    category = (
        ('Leptop','Leptop'),
        ('Mobile','Mobile'),
        ('Camera','Camera'),
        )
    company = (
        ('Dell','Dell'),
        ('Lenovo','Lenovo'),
        ('Hp','Hp'),
        ('Xaiomi','Xaiomi'),
        ('Samsung','Samsung'),
        ('Vivo','Vivo'),
        ('Canon','Canon'),
        ('Nikon','Nikon'),
        ('Fujifilm','Fujifilm'),
        )

    product_seller = models.ForeignKey(User,on_delete=models.CASCADE)
    product_category = models.CharField(max_length=100,choices=category)
    product_company = models.CharField(max_length=100,choices=company)
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField()
    product_price = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='product_image/')



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.fname +"-"+self.products.product_name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    time=models.DateTimeField(default=timezone.now)
    product_price=models.PositiveIntegerField()
    product_qty=models.PositiveIntegerField(default=1)
    total_price=models.PositiveIntegerField()
    status=models.BooleanField(default=False)



class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
