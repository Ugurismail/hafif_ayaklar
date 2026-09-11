from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0062_habit_reminder_enabled_habit_reminder_time_and_more'),
    ]

    operations = [
        # Python name changes, but the existing column and all values stay intact.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name='userprofile', old_name='is_dj',
                    new_name='can_manage_attendance',
                ),
                migrations.AlterField(
                    model_name='userprofile', name='can_manage_attendance',
                    field=models.BooleanField(
                        default=False, db_column='is_dj',
                        verbose_name='Devam Cetveli Yetkisi',
                    ),
                ),
            ],
        ),
    ]
