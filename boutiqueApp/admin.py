from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)