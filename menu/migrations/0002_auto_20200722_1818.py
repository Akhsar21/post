# Generated by Django 3.0.8 on 2020-07-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='anonymous_only',
            field=models.BooleanField(blank=True, default=False, help_text='Should this item only be shown to non-logged-in users?'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='login_required',
            field=models.BooleanField(blank=True, help_text='Should this item only be shown to authenticated users?', null=True),
        ),
    ]
