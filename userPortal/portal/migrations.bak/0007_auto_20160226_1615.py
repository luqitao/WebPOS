# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 08:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20160224_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticateemail',
            name='portal_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='authenticateemailtask',
            name='authenticate_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_email', to='portal.AuthenticateEmail'),
        ),
    ]
