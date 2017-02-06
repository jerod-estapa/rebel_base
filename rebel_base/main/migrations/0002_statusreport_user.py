# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusreport',
            name='user',
            field=models.ForeignKey(to='payments.User'),
        ),
    ]
