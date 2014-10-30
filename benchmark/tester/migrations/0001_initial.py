# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f1', models.CharField(max_length=20)),
                ('f2', models.CharField(max_length=20)),
                ('f3', models.IntegerField()),
                ('f4', models.IntegerField()),
                ('f5', models.DateField()),
                ('f6', models.DateField()),
                ('f7', models.BooleanField(default=False)),
                ('f8', models.BooleanField(default=False)),
                ('f9', models.DateTimeField()),
                ('f10', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
