# Generated by Django 4.1 on 2023-01-22 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.CharField(max_length=200, null=True)),
                ('remark', models.TextField()),
                ('status', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillset', models.CharField(default='', max_length=300)),
                ('introduction', models.CharField(default='', max_length=500, null=True)),
                ('linkedin_url', models.CharField(default='', max_length=200, null=True)),
                ('facebook_url', models.CharField(default='', max_length=200, null=True)),
                ('github_url', models.CharField(default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Freelancer',
                'verbose_name_plural': 'Freelancers',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=webapp.models.upload_path)),
                ('price', models.FloatField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('freelancerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.freelancer')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=200, null=True)),
                ('is_freelancer', models.BooleanField(null=True)),
                ('profile_image', models.ImageField(null=True, upload_to=webapp.models.profile_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=200)),
                ('booking_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.booking')),
                ('to_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.profile')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.AddField(
            model_name='freelancer',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.profile'),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('from_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_userID', to='webapp.profile')),
                ('to_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_userID', to='webapp.profile')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='serviceID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.service'),
        ),
        migrations.AddField(
            model_name='booking',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.profile'),
        ),
    ]
