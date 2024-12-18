# Generated by Django 5.1.2 on 2024-10-28 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_control", "0005_valetkey_resource"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="valetkey",
            name="can_delete",
        ),
        migrations.RemoveField(
            model_name="valetkey",
            name="can_edit",
        ),
        migrations.RemoveField(
            model_name="valetkey",
            name="can_upload",
        ),
        migrations.AlterField(
            model_name="valetkey",
            name="key",
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
    ]
