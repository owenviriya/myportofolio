import uuid

from django.db import migrations


def backfill_uuid_ids(apps, schema_editor):
    connection = schema_editor.connection
    quote = connection.ops.quote_name

    for model_name in ("Education", "Language", "SkillGroup"):
        model = apps.get_model("main", model_name)
        table = quote(model._meta.db_table)
        pk_column = quote(model._meta.pk.column)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {pk_column} FROM {table}")
            old_ids = [row[0] for row in cursor.fetchall()]

            for old_id in old_ids:
                new_id = uuid.uuid4().hex
                cursor.execute(
                    f"UPDATE {table} SET {pk_column} = %s WHERE {pk_column} = %s",
                    [new_id, old_id],
                )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_alter_education_id_alter_language_id_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_uuid_ids),
    ]