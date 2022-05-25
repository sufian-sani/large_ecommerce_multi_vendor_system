from django.contrib import admin
from . models import vendor_registration_table, vendor_payment_info, vendor_PO_NUMBER

# Register your models here.
from import_export.admin import ImportExportModelAdmin


class Bran(ImportExportModelAdmin):
    pass


admin.site.register(vendor_registration_table, Bran)
admin.site.register(vendor_payment_info, Bran)
admin.site.register(vendor_PO_NUMBER, Bran)
