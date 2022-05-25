from django.contrib import admin
from .models import home_benner, home_little_benner, home_bottom_benner, home_side_benner, Shop_now_page_benner
from app_1.models import customer_review
from import_export.admin import ImportExportModelAdmin


class Bran(ImportExportModelAdmin):
    pass


admin.site.register(customer_review, Bran)
admin.site.register(home_benner, Bran)
admin.site.register(home_little_benner, Bran)
admin.site.register(home_bottom_benner, Bran)
admin.site.register(home_side_benner, Bran)
admin.site.register(Shop_now_page_benner, Bran)