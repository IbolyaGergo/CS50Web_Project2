# Generated by Django 4.1.5 on 2023-05-04 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listingmodel_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingmodel',
            name='category',
        ),
    ]
