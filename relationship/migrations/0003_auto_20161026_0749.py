# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationship', '0002_friendship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='id',
        ),
        migrations.RemoveField(
            model_name='imuser',
            name='id',
        ),
        migrations.AddField(
            model_name='friendship',
            name='fsid',
            field=models.AutoField(default='1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='fromid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_sent', to='relationship.IMUser'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='toid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_receive', to='relationship.IMUser'),
        ),
        migrations.AlterField(
            model_name='imuser',
            name='userid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]