# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnpaidUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('last_notification', models.DateTimeField(default=datetime.datetime(2017, 2, 6, 17, 40, 47, 578373))),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('last_4_digits', models.CharField(max_length=4, null=True, blank=True)),
                ('stripe_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rank', models.CharField(max_length=50, default='Padawan')),
                ('badges', models.ManyToManyField(to='main.Badge')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
