# Generated by Django 3.2.6 on 2022-04-26 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20220422_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_table',
            name='Order_Date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 318970)),
        ),
        migrations.AlterField(
            model_name='order_table',
            name='Order_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 318933)),
        ),
        migrations.AlterField(
            model_name='order_table',
            name='Paid_Date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 318986)),
        ),
        migrations.AlterField(
            model_name='order_table',
            name='Paid_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 318955)),
        ),
        migrations.AlterField(
            model_name='order_table_2',
            name='Order_Date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 320301)),
        ),
        migrations.AlterField(
            model_name='order_table_3_logs',
            name='logs_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 323965)),
        ),
        migrations.AlterField(
            model_name='order_table_logs',
            name='logs_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 323359)),
        ),
    ]