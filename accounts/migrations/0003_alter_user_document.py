# Generated by Django 3.2.4 on 2021-09-21 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210921_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='document',
            field=models.ImageField(blank=True, null=True, upload_to='merchant documents'),
        ),
    ]
