# Generated by Django 2.0 on 2018-02-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20180128_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='deposit',
            field=models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('DASH', 'DASH')], max_length=30),
        ),
        migrations.AlterField(
            model_name='credit',
            name='format_lain',
            field=models.CharField(choices=[('Y', 'Y'), ('M', 'M'), ('D', 'D')], max_length=30),
        ),
        migrations.AlterField(
            model_name='credit',
            name='lain',
            field=models.CharField(choices=[('USD', 'USD'), ('RUR', 'RUB')], max_length=30),
        ),
    ]