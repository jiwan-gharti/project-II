# Generated by Django 3.2.4 on 2021-09-15 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_rename_order_shippingaddress_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order_item',
        ),
    ]