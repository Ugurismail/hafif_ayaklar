# Generated by Django 4.2.2 on 2025-01-29 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_userprofile_pagination_active_background_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='yanit_card',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
