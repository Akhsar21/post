# Generated by Django 3.0.7 on 2020-06-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20200626_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(default='avatar.png', upload_to='avatars'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
