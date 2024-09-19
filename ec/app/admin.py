from django.contrib import admin
from . models import Product
from . models import PlasticItem
from . models import Customer
from . models import Cart

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']
   

# Register your models here
@admin.register(PlasticItem)
class PlasticItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'basic_quantity', 'supercoins_for_basic_quantity', 'plastic_image']
    
    
@admin.register(Customer)   
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality','city','state', 'zipcode']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    
    
from django.contrib import admin
from .models import OrderPlaced, Payment

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'product', 'plastic_item', 'quantity', 'status', 'ordered_date', 'payment']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'customer__name', 'product__title', 'plastic_item__type']
    ordering = ['-ordered_date']
    list_editable = ['status']  # Allows changing status directly from the list view

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'paid']
    list_filter = ['paid', 'razorpay_payment_status']
    search_fields = ['user__username', 'razorpay_order_id', 'razorpay_payment_id']
    ordering = ['-id']

admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)

