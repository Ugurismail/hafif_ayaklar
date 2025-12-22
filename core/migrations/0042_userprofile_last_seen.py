from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0041_merge_20251212_2046"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="last_seen",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

