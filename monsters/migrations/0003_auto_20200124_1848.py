# Generated by Django 3.0.2 on 2020-01-24 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='path/media/images/150x150.png', upload_to='images/'),
        ),
    ]