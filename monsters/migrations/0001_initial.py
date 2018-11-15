# Generated by Django 2.1.3 on 2018-11-14 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MonsterReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('monster', models.ManyToManyField(to='monsters.Monster')),
                ('researcher', models.ManyToManyField(to='monsters.Researcher')),
            ],
        ),
        migrations.AddField(
            model_name='monsterreport',
            name='sighting',
            field=models.ManyToManyField(to='monsters.Sighting'),
        ),
    ]
