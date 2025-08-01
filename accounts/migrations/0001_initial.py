# Generated by Django 4.1 on 2025-07-24 16:42

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ameneties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(upload_to='hotels')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=100)),
                ('hotel_description', models.TextField()),
                ('hotel_slug', models.SlugField(max_length=1000, unique=True)),
                ('hotel_price', models.FloatField()),
                ('hotel_offer_price', models.FloatField()),
                ('hotel_location', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('ameneties', models.ManyToManyField(to='accounts.ameneties')),
            ],
        ),
        migrations.CreateModel(
            name='HotelUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(upload_to='profile')),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('email_token', models.CharField(blank=True, max_length=100, null=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HotelVendor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(upload_to='profile')),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('email_token', models.CharField(blank=True, max_length=100, null=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HotelManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=100)),
                ('manager_contact', models.CharField(max_length=100)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_managers', to='accounts.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotels')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='accounts.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='accounts.hotelvendor'),
        ),
    ]
