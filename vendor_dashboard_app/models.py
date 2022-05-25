from django.db import models
from datetime import datetime
# Create your models here.

class vendor_registration_table(models.Model):
    vendor_name = models.CharField(max_length=40)
    vendor_shop_name = models.CharField(max_length=100)
    vendor_shop_url = models.TextField(blank=True, null=True)
    vendor_address = models.CharField(max_length=200, blank=True, null=True)
    vendor_shop_logo = models.TextField(blank=True, null=True)
    vendor_shop_banner = models.TextField(blank=True, null=True)
    vendor_phone_no = models.CharField(max_length=100)
    vendor_email = models.EmailField(max_length=100)
    vendor_password = models.CharField(max_length=100)
    vendor_activation = models.BooleanField(default=False)
    join_date = models.DateField(default=datetime.now(), blank=True)
    
    featured_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_shop_name


class vendor_payment_info(models.Model):
    Vendor = models.ForeignKey(vendor_registration_table, on_delete=models.CASCADE)
    payment_roll = (
        ("SSLCommerz", "SSLCommerz"),
        ("Bank Deposite", "Bank Deposite"),
    )
    vendor_payment_roll = models.CharField(max_length=20, choices=payment_roll, default="SSLCommerz")
    Bank_Name = models.CharField(max_length=200,blank=True, null=True)
    Account_Name = models.CharField(max_length=200,blank=True, null=True)
    Account_Number = models.IntegerField(blank=True, null=True)
    Branch = models.CharField(max_length=200, blank=True, null=True)
    Routing_Number = models.IntegerField(blank=True, null=True)
    SSL_operator_role = (

        ("Bkash", "Bkash"),
        ("Nogod", "Nogod"),
    )
    SSL_operator = models.CharField(max_length=20, choices=SSL_operator_role, blank=True, null=True)
    SSL_Mobile_Number = models.IntegerField(blank=True, null=True)


class vendor_PO_NUMBER(models.Model):
    Vendor = models.ForeignKey(vendor_registration_table, on_delete=models.CASCADE)
    Vendor_po_Number = models.IntegerField()
