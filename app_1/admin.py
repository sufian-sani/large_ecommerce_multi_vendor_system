from django.contrib import admin
from .models import Category, Subcategory_1, Subcategory_2, Brand, Products, Staff_Access, Flash_Sell, attribute_connect_with_product, campaign_product_attribute, Attribute
# Register your models here.
from .models import User
from import_export.admin import ImportExportModelAdmin


class Bran(ImportExportModelAdmin):
    pass


admin.site.register(User, Bran)

admin.site.register(Category, Bran),
admin.site.register(Subcategory_1, Bran),
admin.site.register(Subcategory_2, Bran),
admin.site.register(Brand, Bran),
admin.site.register(Products, Bran),
admin.site.register(Staff_Access, Bran),
admin.site.register(Attribute, Bran),


admin.site.register(attribute_connect_with_product, Bran),

admin.site.register(Flash_Sell, Bran)

admin.site.register(campaign_product_attribute, Bran)