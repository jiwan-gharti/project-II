# Generated by Django 3.2.4 on 2021-10-03 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20211002_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='sentiment',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
