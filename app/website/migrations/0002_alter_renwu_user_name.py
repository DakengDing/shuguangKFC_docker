# Generated by Django 4.2 on 2023-04-17 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renwu',
            name='user_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]