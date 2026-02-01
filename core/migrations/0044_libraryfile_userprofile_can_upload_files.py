from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_alter_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='can_upload_files',
            field=models.BooleanField(default=False, verbose_name='Dosya Yukleme Yetkisi'),
        ),
        migrations.CreateModel(
            name='LibraryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Baslik')),
                ('description', models.TextField(blank=True, verbose_name='Aciklama')),
                ('file', models.FileField(upload_to='library_files/', verbose_name='Dosya')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
