# Generated by Django 3.0.7 on 2020-06-21 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monster_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='untilted', max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]