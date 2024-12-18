# Generated by Django 5.1.2 on 2024-10-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_control", "0003_resource_delete_imageupload_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="valetkey",
            name="can_delete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="valetkey",
            name="can_edit",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="valetkey",
            name="can_upload",
            field=models.BooleanField(default=False),
        ),
    ]
