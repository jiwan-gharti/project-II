# Generated by Django 3.2.4 on 2021-10-02 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20211002_1423'),
        ('myprofile', '0004_alter_merchantreview_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.orderitem'),
        ),
    ]