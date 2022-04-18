from django.contrib import admin
from .models import *
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
	list_display = ('name','email','message')


class ProductsAdmin(admin.ModelAdmin):
	list_display =('product_seller','product_category','product_company','product_name','product_price')


class TransactionAdmin(admin.ModelAdmin):
	list_display=('made_by','made_on','amount','order_id')


admin.site.register(Contact,ContactAdmin)

admin.site.register(User)

admin.site.register(Products,ProductsAdmin)

admin.site.register(Wishlist)

admin.site.register(Cart)

admin.site.register(Transaction,TransactionAdmin)