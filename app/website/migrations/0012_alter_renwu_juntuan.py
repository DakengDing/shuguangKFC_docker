# Generated by Django 4.2 on 2023-05-03 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_jiandui_fc_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renwu',
            name='juntuan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.juntuan'),
        ),
    ]
