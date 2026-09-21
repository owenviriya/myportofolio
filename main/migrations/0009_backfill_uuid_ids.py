import uuid

from django.db import migrations


def backfill_uuid_ids(apps, schema_editor):
    database = schema_editor.connection.alias

    for model_name in ("Education", "Language", "SkillGroup"):
        model = apps.get_model("main", model_name)
        manager = model._base_manager.using(database)

        for record in manager.only("pk").iterator(chunk_size=500):
            manager.filter(pk=record.pk).update(**{model._meta.pk.name: uuid.uuid4()})


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_alter_education_id_alter_language_id_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_uuid_ids),
    ]
