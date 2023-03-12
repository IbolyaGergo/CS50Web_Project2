# Generated by Django 4.1.5 on 2023-03-01 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('img', models.ImageField(upload_to='images/')),
                ('start_bid', models.DecimalField(decimal_places=2, max_digits=64)),
            ],
        ),
    ]