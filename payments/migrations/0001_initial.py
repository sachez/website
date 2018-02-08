# Generated by Django 2.0 on 2018-01-23 22:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=35, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('ver_inform_upload', models.BooleanField(default=False)),
                ('ver_inform_approve', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('take_credit', 'Can take credit'),),
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.CharField(choices=[('BTC', 'BitCoin'), ('ETH', 'Etheryum'), ('LTC', 'LaitCoin'), ('RDD', 'RedCoin')], default='BTC', max_length=50)),
                ('summary_depos', models.IntegerField()),
                ('lain', models.CharField(choices=[('USD', 'Dollars'), ('RUB', 'Russin_Fed_Rubblers')], default='USD', max_length=50)),
                ('max_lain', models.IntegerField()),
                ('format_lain', models.CharField(choices=[('M', 'Months'), ('D', 'Days'), ('Y', 'Years')], default='months', max_length=50)),
                ('time_lain', models.IntegerField()),
                ('date_credit', models.DateField(auto_now_add=True)),
                ('approve', models.NullBooleanField()),
                ('fo_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='user@mail.ru', max_length=254)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('adress', models.CharField(max_length=100)),
                ('pasport', models.ImageField(upload_to='pasports/')),
                ('note_bank', models.ImageField(upload_to='note_banks/')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
