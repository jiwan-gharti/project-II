# Generated by Django 3.2.4 on 2021-09-22 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='inventory', to='mainapp.productinventory', verbose_name='Quantity'),
        ),
    ]
