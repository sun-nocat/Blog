# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-07 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20181107_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images')),
                ('image_name', models.CharField(max_length=50)),
                ('width', models.CharField(max_length=10, null=True)),
                ('height', models.CharField(max_length=10, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]
