# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArmyRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'full', max_length=4, choices=[(b'full', 'Army full'), (b'arch', 'Archers'), (b'capt', 'Captain')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('village', models.ForeignKey(to='core.Village')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='armyrequest',
            unique_together=set([('user', 'village', 'type')]),
        ),
    ]
