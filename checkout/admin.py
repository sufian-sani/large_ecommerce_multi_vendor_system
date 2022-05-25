from django.contrib import admin
from .models import Customer_delivery_information, Order_Table, Order_Table_2, order_table_logs, Order_Table_3
# Register your models here.
from import_export.admin import ImportExportModelAdmin


class Bran(ImportExportModelAdmin):
    pass

admin.site.register(Customer_delivery_information, Bran)
admin.site.register(Order_Table, Bran)
admin.site.register(Order_Table_2, Bran)
admin.site.register(order_table_logs, Bran)
admin.site.register(Order_Table_3, Bran)