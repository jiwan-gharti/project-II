# Generated by Django 3.2.4 on 2021-10-01 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myprofile',
            options={'verbose_name': 'Customer Profile', 'verbose_name_plural': 'Customer Profile'},
        ),
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'verbose_name': 'Customer Shipping Address', 'verbose_name_plural': 'Customer Shipping Address'},
        ),
    ]
