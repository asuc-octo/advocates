# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 19:45
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Open', max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('division', models.CharField(choices=[('Academic', (('Grade Appeals', 'Grade Appeals'), ('Enrollment', 'Enrollment'), ('Withdrawal', 'Withdrawal'), ('Unfair Testing', 'Unfair Testing'))), ('Financial Aid', (('Financial Aid', 'Financial Aid'), ('Residency for Tuition', 'Residency for Tuition'), ('SHIP', 'SHIP'))), ('Conduct and Grievance', (('Drugs and Alcohol', 'Drugs and Alcohol'), ('Sexual Assault', 'Sexual Assault')))], max_length=200)),
                ('open_date', models.DateTimeField(verbose_name='date created')),
                ('last_update', models.DateTimeField(verbose_name='last update date')),
                ('notes', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='CaseWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('permissions', models.CharField(choices=[('General', 'General'), ('Director', 'Director'), ('Policy Coordinator', 'Policy Coordinator'), ('Chief of Staff', 'Chief of Staff'), ('Student Advocate', 'Student Advocate')], max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime(2017, 3, 20, 19, 45, 50, 290255, tzinfo=utc), verbose_name='date comment created')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='caseworker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cw', to='cases.CaseWorker'),
        ),
        migrations.AddField(
            model_name='case',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
