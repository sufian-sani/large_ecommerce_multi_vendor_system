# Generated by Django 3.2.6 on 2022-04-26 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0003_auto_20220422_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign_table',
            name='end_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 310211), null=True),
        ),
        migrations.AlterField(
            model_name='campaign_table',
            name='start_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 310189), null=True),
        ),
        migrations.AlterField(
            model_name='customer_review',
            name='Review_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 307350)),
        ),
        migrations.AlterField(
            model_name='flash_sell',
            name='flash_sell_end_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 309153)),
        ),
        migrations.AlterField(
            model_name='flash_sell',
            name='flash_sell_start_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 309126)),
        ),
        migrations.AlterField(
            model_name='products',
            name='Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 304138)),
        ),
        migrations.AlterField(
            model_name='products',
            name='flash_sell_end_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 304205)),
        ),
        migrations.AlterField(
            model_name='products',
            name='flash_sell_start_time',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 304189)),
        ),
        migrations.AlterField(
            model_name='staff_access',
            name='First_Register_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 309643)),
        ),
        migrations.AlterField(
            model_name='staff_access',
            name='Last_login_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 26, 16, 0, 10, 309665)),
        ),
    ]
