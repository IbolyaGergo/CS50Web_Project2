# Generated by Django 4.1.5 on 2023-04-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listingmodel_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingmodel',
            name='winner',
            field=models.CharField(default='', max_length=64),
        ),
    ]
