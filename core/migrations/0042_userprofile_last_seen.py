from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0040_kenarda_draft_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="last_seen",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
