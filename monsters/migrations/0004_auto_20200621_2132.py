# Generated by Django 3.0.7 on 2020-06-21 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0003_monster_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster_image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/monsters/images/'),
        ),
    ]