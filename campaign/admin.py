from django.contrib import admin
from app_1.models import campaign_product_table, campaign_table, campaign_categories_percentage
# Register your models here.


admin.site.register(campaign_table)
admin.site.register(campaign_categories_percentage)

admin.site.register(campaign_product_table)