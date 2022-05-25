from django.db import models
from app_1.models import User
from app_1.models import Products, Staff_Access, campaign_table, Category, attribute_connect_with_product
from datetime import datetime
# Create your models here.
from vendor_dashboard_app .models import vendor_registration_table
import uuid

from django.core.validators import FileExtensionValidator


class Customer_delivery_information(models.Model):
    class Meta:
        verbose_name_plural = 'Customer Delivery Information'
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Street_Address = models.CharField(max_length=255)
    Town_City = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    Post_Code = models.CharField(max_length=255)
    Phone_Number = models.CharField(max_length=255)
    Email_Address = models.CharField(max_length=255)

    def __str__(self):
        return self.First_Name + " " + self.Last_Name


class Order_Table(models.Model):
    class Meta:
        verbose_name_plural = 'Order Table'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    Customer_delivery_information = models.ForeignKey(Customer_delivery_information, on_delete=models.CASCADE)
    Order_Id = models.CharField(max_length=255, blank=True, null=True)
    SubTotal_Price=models.IntegerField(blank=True, null=True)
    Delivery_Charge=models.IntegerField(blank=True, null=True)
    GrandTotal_Price = models.IntegerField(blank=True, null=True)
    Partial_Price = models.IntegerField(blank=True, null=True, default='0')
    Due_price = models.IntegerField(blank=True, null=True, default='0')
    Vendor_qty = models.IntegerField(blank=True, null=True)
    Holder_Name = models.CharField(max_length=255, blank=True, null=True)
    Bank_Name = models.CharField(max_length=255, blank=True, null=True)
    Branch_Name = models.CharField(max_length=255, blank=True, null=True)
    Account_Number = models.CharField(max_length=255, blank=True, null=True)
    Slip_Number = models.CharField(max_length=255, blank=True, null=True)
    Deposit_slip = models.FileField(upload_to='Deposit_Slip', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])], help_text = "Choose Only .jpg, .jpeg, .png and files PLease..")

    Order_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Paid_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Order_Date = models.DateField(default=datetime.now(), blank=True)
    Paid_Date = models.DateField(default=datetime.now(), blank=True)
    Status = (
        ("Pending payment", "Pending payment"),
        ("Partially Paid", "Partially Paid"),
        ("Ready To Ship", "Ready To Ship"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
        ("Picked", "Picked"),
        ("On hold", "On hold"),
        ("Failed", "Failed"),
    )
    Order_Status = models.CharField(max_length=20, choices=Status, default="Pending payment")
    Payment_Type_Status = (
        ("Full", "Full"),
        ("Partially", "Partially"),
    )
    Payment_Type = models.CharField(max_length=20, choices=Payment_Type_Status, default="Full")
    shipping_status = (
        ("Pickup From BoomBoom Office", "Pickup From BoomBoom Office"),
        ("Delivery", "Delivery"),
    )
    Shopping = models.CharField(max_length=100, choices=shipping_status, default="Pickup From BoomBoom Office")
    shipping_note= models.CharField(max_length=255, blank=True, null=True)
    Payment_method_Status = (
        ("Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)", "Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)"),
        ("Pay With Nagad", "Pay With Nagad"),
        ("Pay With Bkash", "Pay With Bkash"),
        ("Bank Deposit", "Bank Deposit"),
        ("COD", "COD"),
    )
    Payment_method = models.CharField(max_length=100, choices=Payment_method_Status, default="Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)")
    Cam_Status = (
        ("Reguler", "Reguler"),
        ("Campaign", "Campaign"),
    )
    Campaign_Status = models.CharField(max_length=20, choices=Cam_Status, default="Reguler")
    Order_Campaign = models.ForeignKey(campaign_table, on_delete=models.CASCADE, blank=True, null=True, default='1')
    Order_Note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Order_Id

    # def save(self, *args, **kwargs):
    #     if not Order_Table.objects.count():
    #         self.Order_Id = 30000
    #     else:
    #         self.Order_Id = int(Order_Table.objects.last().Order_Id) + 1
    #     super(Order_Table, self).save(*args, **kwargs)




class Order_Table_2(models.Model):
    class Meta:
        verbose_name_plural = 'Order Table 2'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Order_Id = models.ForeignKey(Order_Table, on_delete=models.CASCADE)
    New_Order_Id = models.CharField(max_length=100, blank=True, null=True)
    Status = (
        ("", ""),
        ("Pending payment", "Pending payment"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
        ("Picked", "Picked"),
        ("On hold", "On hold"),
        ("Failed", "Failed"),
    )
    New_Order_Status = models.CharField(max_length=20, choices=Status, default="", blank=True, null=True)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Attribute = models.ForeignKey(attribute_connect_with_product, on_delete=models.CASCADE, blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default='1')
    Vendors = models.ForeignKey(vendor_registration_table, on_delete=models.CASCADE, blank=True, null=True)
    MRP_price = models.IntegerField()
    Cost_price = models.IntegerField()
    then_price = models.IntegerField()
    Quantity = models.IntegerField()
    SubTotal_Price = models.IntegerField()
    Campaign = models.ForeignKey(campaign_table, on_delete=models.CASCADE, blank=True, null=True)
    Order_Date = models.DateField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.Order_Id.Order_Id



class Order_Table_3(models.Model):
    class Meta:
        verbose_name_plural = 'Order Table 3'

    old_order_id = models.CharField(max_length=200, blank=True, null=True)
    old_customer_first_name = models.CharField(max_length=200, blank=True, null=True)
    old_customer_last_name = models.CharField(max_length=200, blank=True, null=True)
    old_unq_number = models.IntegerField()
    old_order_date = models.DateField(blank=True, null=True)
    old_paid_date = models.DateField(blank=True, null=True)
    old_Status = (

        ("", ""),
        ("Pending Payment", "Pending Payment"),
        ("Processing", "Processing"),
        ("Refunded", "Refunded"),
        ("Partially Paid", "Partially Paid"),
        ("Cancelled", "Cancelled"),
        ("Shifted To Courier", "Shifted To Courier"),
        ("Picked", "Picked"),
        ("Completed", "Completed"),
        ("On Hold", "On Hold"),
        ("Cash On Delivery", "Cash On Delivery"),

    )
    old_order_status = models.CharField(max_length=200, choices=old_Status, default="", blank=True, null=True)
    old_order_total = models.IntegerField(blank=True, null=True)
    old_Subtotal_Amount = models.IntegerField(blank=True, null=True)
    old_delivery_charge = models.IntegerField(blank=True, null=True)
    old_greand_total = models.IntegerField(blank=True, null=True)
    old_Shopping_method = models.CharField(max_length=200, blank=True, null=True)
    old_Payment_method = models.CharField(max_length=200, blank=True, null=True)
    old_Customer_Address = models.CharField(max_length=200, blank=True, null=True)
    old_Customer_City = models.CharField(max_length=200, blank=True, null=True)
    old_Customer_Postcode = models.CharField(max_length=200, blank=True, null=True)
    old_Customer_Email = models.EmailField(max_length=200, blank=True, null=True)
    old_Customer_Phone = models.CharField(max_length=200, blank=True, null=True)
    old_product_1 = models.CharField(max_length=20, blank=True, null=True)
    old_product_1_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_1_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_2 = models.CharField(max_length=200, blank=True, null=True)
    old_product_2_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_2_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_3 = models.CharField(max_length=200, blank=True, null=True)
    old_product_3_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_3_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_4 = models.CharField(max_length=200, blank=True, null=True)
    old_product_4_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_4_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_5 = models.CharField(max_length=200, blank=True, null=True)
    old_product_5_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_5_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_6 = models.CharField(max_length=200, blank=True, null=True)
    old_product_6_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_6_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_7 = models.CharField(max_length=200, blank=True, null=True)
    old_product_7_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_7_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_8 = models.CharField(max_length=200, blank=True, null=True)
    old_product_8_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_8_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_9 = models.CharField(max_length=200, blank=True, null=True)
    old_product_9_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_9_price = models.IntegerField(blank=True, null=True, default=None)
    old_product_10 = models.CharField(max_length=200, blank=True, null=True)
    old_product_10_quenity = models.CharField(max_length=20, blank=True, null=True)
    old_product_10_price = models.IntegerField(blank=True, null=True, default=None)

    def multiply_p1(self):
        m_p = int(self.old_product_1_quenity)*self.old_product_1_price
        return m_p


    def multiply_p2(self):
        if self.old_product_2:
            m_p = int(self.old_product_2_quenity)*self.old_product_2_price
            return m_p


    def multiply_p3(self):
        if self.old_product_3:
            m_p = int(self.old_product_3_quenity)*self.old_product_3_price
            return m_p

    def multiply_p4(self):
        if self.old_product_4:
            m_p = int(self.old_product_4_quenity) * self.old_product_4_price
            return m_p

    def multiply_p5(self):
        if self.old_product_5:
            m_p = int(self.old_product_5_quenity)*self.old_product_5_price
            return m_p


    def multiply_p6(self):
        if self.old_product_6:
            m_p = int(self.old_product_6_quenity)*self.old_product_6_price
            return m_p

    def multiply_p7(self):
        if self.old_product_7:
            m_p = int(self.old_product_7_quenity)*self.old_product_7_price
            return m_p


    def multiply_p8(self):
        if self.old_product_8:
            m_p = int(self.old_product_8_quenity)*self.old_product_8_price
            return m_p


    def multiply_p9(self):
        if self.old_product_9:
            m_p = int(self.old_product_9_quenity)*self.old_product_9_price
            return m_p


    def multiply_p10(self):
        if self.old_product_10:
            m_p = int(self.old_product_10_quenity)*self.old_product_10_price
            return m_p



class order_table_logs(models.Model):
    class Meta:
        verbose_name_plural = 'Order Table Logs'
    staff_role = models.ForeignKey(Staff_Access, on_delete=models.CASCADE, blank=True, null=True)
    order_table_1 = models.ForeignKey(Order_Table, on_delete=models.CASCADE, blank=True, null=True, default='1')
    logs_status = models.TextField(blank=True, null=True)
    logs_time = models.DateTimeField(default=datetime.now(), blank=True)




class order_table_3_logs(models.Model):
    class Meta:
        verbose_name_plural = 'Order Table 3 Logs'
    staff_role = models.ForeignKey(Staff_Access, on_delete=models.CASCADE, blank=True, null=True)
    order_table_3 = models.ForeignKey(Order_Table_3, on_delete=models.CASCADE, blank=True, null=True, default='1')
    logs_status = models.TextField(blank=True, null=True)
    logs_time = models.DateTimeField(default=datetime.now(), blank=True)