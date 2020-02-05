from django.contrib import admin
from .models import Signup


# class OrderAdminInline(admin.TabularInline):
#     model = Order


# class OrderAdmin(admin.ModelAdmin):
#     inlines = (OrderAdminInline, )


admin.site.register(Signup)
# admin.site.register(Order)