# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 05:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0003_auto_20161228_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(blank=True, verbose_name='リプライ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='comment',
            new_name='comments',
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cms.File', verbose_name='コメント'),
        ),
        migrations.AddField(
            model_name='reply',
            name='comments',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='cms.Comments', verbose_name='リプライ'),
        ),
    ]
