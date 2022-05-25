# Generated by Django 3.2.6 on 2022-04-22 10:57

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor_dashboard_app', '0002_alter_vendor_registration_table_join_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_1', '0002_auto_20220422_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_delivery_information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=255)),
                ('Last_Name', models.CharField(max_length=255)),
                ('Street_Address', models.CharField(max_length=255)),
                ('Town_City', models.CharField(max_length=255)),
                ('District', models.CharField(max_length=255)),
                ('Post_Code', models.CharField(max_length=255)),
                ('Phone_Number', models.CharField(max_length=255)),
                ('Email_Address', models.CharField(max_length=255)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Delivery Information',
            },
        ),
        migrations.CreateModel(
            name='Order_Table',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Order_Id', models.CharField(blank=True, max_length=255, null=True)),
                ('SubTotal_Price', models.IntegerField(blank=True, null=True)),
                ('Delivery_Charge', models.IntegerField(blank=True, null=True)),
                ('GrandTotal_Price', models.IntegerField(blank=True, null=True)),
                ('Partial_Price', models.IntegerField(blank=True, default='0', null=True)),
                ('Due_price', models.IntegerField(blank=True, default='0', null=True)),
                ('Vendor_qty', models.IntegerField(blank=True, null=True)),
                ('Holder_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Bank_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Branch_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Account_Number', models.CharField(blank=True, max_length=255, null=True)),
                ('Slip_Number', models.CharField(blank=True, max_length=255, null=True)),
                ('Deposit_slip', models.FileField(blank=True, help_text='Choose Only .jpg, .jpeg, .png and files PLease..', null=True, upload_to='Deposit_Slip', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('Order_Time', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 94452))),
                ('Paid_Time', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 94452))),
                ('Order_Date', models.DateField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 94452))),
                ('Paid_Date', models.DateField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 94452))),
                ('Order_Status', models.CharField(choices=[('Pending payment', 'Pending payment'), ('Partially Paid', 'Partially Paid'), ('Ready To Ship', 'Ready To Ship'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'), ('Picked', 'Picked'), ('On hold', 'On hold'), ('Failed', 'Failed')], default='Pending payment', max_length=20)),
                ('Payment_Type', models.CharField(choices=[('Full', 'Full'), ('Partially', 'Partially')], default='Full', max_length=20)),
                ('Shopping', models.CharField(choices=[('Pickup From BoomBoom Office', 'Pickup From BoomBoom Office'), ('Delivery', 'Delivery')], default='Pickup From BoomBoom Office', max_length=100)),
                ('shipping_note', models.CharField(blank=True, max_length=255, null=True)),
                ('Payment_method', models.CharField(choices=[('Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)', 'Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)'), ('Pay With Nagad', 'Pay With Nagad'), ('Pay With Bkash', 'Pay With Bkash'), ('Bank Deposit', 'Bank Deposit'), ('COD', 'COD')], default='Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)', max_length=100)),
                ('Campaign_Status', models.CharField(choices=[('Reguler', 'Reguler'), ('Campaign', 'Campaign')], default='Reguler', max_length=20)),
                ('Order_Note', models.TextField(blank=True, null=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Customer_delivery_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.customer_delivery_information')),
                ('Order_Campaign', models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_1.campaign_table')),
            ],
            options={
                'verbose_name_plural': 'Order Table',
            },
        ),
        migrations.CreateModel(
            name='Order_Table_3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('old_customer_first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('old_customer_last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('old_unq_number', models.IntegerField()),
                ('old_order_date', models.DateField(blank=True, null=True)),
                ('old_paid_date', models.DateField(blank=True, null=True)),
                ('old_order_status', models.CharField(blank=True, choices=[('', ''), ('Pending Payment', 'Pending Payment'), ('Processing', 'Processing'), ('Refunded', 'Refunded'), ('Partially Paid', 'Partially Paid'), ('Cancelled', 'Cancelled'), ('Shifted To Courier', 'Shifted To Courier'), ('Picked', 'Picked'), ('Completed', 'Completed'), ('On Hold', 'On Hold'), ('Cash On Delivery', 'Cash On Delivery')], default='', max_length=200, null=True)),
                ('old_order_total', models.IntegerField(blank=True, null=True)),
                ('old_Subtotal_Amount', models.IntegerField(blank=True, null=True)),
                ('old_delivery_charge', models.IntegerField(blank=True, null=True)),
                ('old_greand_total', models.IntegerField(blank=True, null=True)),
                ('old_Shopping_method', models.CharField(blank=True, max_length=200, null=True)),
                ('old_Payment_method', models.CharField(blank=True, max_length=200, null=True)),
                ('old_Customer_Address', models.CharField(blank=True, max_length=200, null=True)),
                ('old_Customer_City', models.CharField(blank=True, max_length=200, null=True)),
                ('old_Customer_Postcode', models.CharField(blank=True, max_length=200, null=True)),
                ('old_Customer_Email', models.EmailField(blank=True, max_length=200, null=True)),
                ('old_Customer_Phone', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_1', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_1_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_1_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_2', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_2_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_2_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_3', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_3_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_3_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_4', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_4_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_4_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_5', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_5_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_5_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_6', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_6_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_6_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_7', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_7_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_7_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_8', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_8_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_8_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_9', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_9_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_9_price', models.IntegerField(blank=True, default=None, null=True)),
                ('old_product_10', models.CharField(blank=True, max_length=200, null=True)),
                ('old_product_10_quenity', models.CharField(blank=True, max_length=20, null=True)),
                ('old_product_10_price', models.IntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Order Table 3',
            },
        ),
        migrations.CreateModel(
            name='order_table_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logs_status', models.TextField(blank=True, null=True)),
                ('logs_time', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 99438))),
                ('order_table_1', models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.CASCADE, to='checkout.order_table')),
                ('staff_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_1.staff_access')),
            ],
            options={
                'verbose_name_plural': 'Order Table Logs',
            },
        ),
        migrations.CreateModel(
            name='order_table_3_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logs_status', models.TextField(blank=True, null=True)),
                ('logs_time', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 99438))),
                ('order_table_3', models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.CASCADE, to='checkout.order_table_3')),
                ('staff_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_1.staff_access')),
            ],
            options={
                'verbose_name_plural': 'Order Table 3 Logs',
            },
        ),
        migrations.CreateModel(
            name='Order_Table_2',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('New_Order_Id', models.CharField(blank=True, max_length=100, null=True)),
                ('New_Order_Status', models.CharField(blank=True, choices=[('', ''), ('Pending payment', 'Pending payment'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'), ('Picked', 'Picked'), ('On hold', 'On hold'), ('Failed', 'Failed')], default='', max_length=20, null=True)),
                ('MRP_price', models.IntegerField()),
                ('Cost_price', models.IntegerField()),
                ('then_price', models.IntegerField()),
                ('Quantity', models.IntegerField()),
                ('SubTotal_Price', models.IntegerField()),
                ('Order_Date', models.DateField(blank=True, default=datetime.datetime(2022, 4, 22, 16, 57, 6, 95449))),
                ('Attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_1.attribute_connect_with_product')),
                ('Campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_1.campaign_table')),
                ('Category', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='app_1.category')),
                ('Order_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.order_table')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_1.products')),
                ('Vendors', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor_dashboard_app.vendor_registration_table')),
            ],
            options={
                'verbose_name_plural': 'Order Table 2',
            },
        ),
    ]
