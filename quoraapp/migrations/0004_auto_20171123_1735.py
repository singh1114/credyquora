# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 17:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quoraapp', '0003_auto_20171123_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upvote',
            old_name='upvotes',
            new_name='upvote',
        ),
    ]
