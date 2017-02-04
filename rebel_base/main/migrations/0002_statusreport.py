# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '__first__'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusReport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to='payments.User')),
            ],
        ),
    ]
