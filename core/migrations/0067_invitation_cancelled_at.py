from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0066_invitation_transfer')]

    operations = [
        migrations.AddField(
            model_name='invitation', name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
