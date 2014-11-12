# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='region_name', db_index=True)),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.IntegerField(unique=True, serialize=False, verbose_name='village_id', primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='village_name', db_index=True)),
                ('x', models.FloatField(verbose_name='village_coordinate_x')),
                ('y', models.FloatField(verbose_name='village_coordinate_y')),
                ('region', models.ForeignKey(default=None, verbose_name='village_region', to='core.Region', null=True)),
            ],
            options={
                'verbose_name': 'village',
                'verbose_name_plural': 'villages',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='village',
            unique_together=set([('x', 'y')]),
        ),
        migrations.AlterIndexTogether(
            name='village',
            index_together=set([('x', 'y')]),
        ),
    ]
