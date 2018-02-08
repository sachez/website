# Generated by Django 2.0 on 2018-01-28 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='deposit',
            field=models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('DASH', 'DASH'), ('DOGE', 'DOGE')], default='BTC', max_length=50),
        ),
        migrations.AlterField(
            model_name='credit',
            name='lain',
            field=models.CharField(choices=[('USD', 'USD'), ('RUR', 'RUB')], default='USD', max_length=50),
        ),
    ]
