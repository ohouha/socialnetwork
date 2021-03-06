# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-14 19:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialnetwork', '0010_follow_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to='socialnetwork.Person')),
                ('to_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to='socialnetwork.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='follow',
            name='people',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.DeleteModel(
            name='follow',
        ),
        migrations.AddField(
            model_name='person',
            name='relationships',
            field=models.ManyToManyField(related_name='related_to', through='socialnetwork.Relationship', to='socialnetwork.Person'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
