from django.db import migrations, models
from django.utils import timezone


def initialize_online_chat_read_at(apps, schema_editor):
    UserProfile = apps.get_model('core', 'UserProfile')
    UserProfile.objects.filter(online_chat_last_read_at__isnull=True).update(
        online_chat_last_read_at=timezone.now()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_visitsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='online_chat_last_read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(initialize_online_chat_read_at, migrations.RunPython.noop),
    ]
