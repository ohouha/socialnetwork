# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-13 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0003_delete_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]