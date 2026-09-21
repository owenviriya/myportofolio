import uuid

from django.db import migrations, models
from django.db.migrations.state import ModelState


MODEL_NAMES = ("Education", "Language", "SkillGroup")
BATCH_SIZE = 500


def replace_integer_primary_keys_with_uuid(apps, schema_editor):
    """Rebuild the affected tables so PostgreSQL never casts bigint to uuid."""
    database = schema_editor.connection.alias

    for model_name in MODEL_NAMES:
        model = apps.get_model("main", model_name)
        temp_table = f"{model._meta.db_table}_uuid_tmp"
        temporary_fields = []

        for field in model._meta.local_fields:
            if field.primary_key:
                uuid_field = models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                )
                temporary_fields.append((field.name, uuid_field))
            else:
                temporary_fields.append((field.name, field.clone()))

        temporary_state = ModelState(
            app_label=model._meta.app_label,
            name=f"{model.__name__}UUIDMigrationTemp",
            fields=temporary_fields,
            options={"db_table": temp_table},
            bases=(models.Model,),
        )
        temporary_model = temporary_state.render(apps)
        schema_editor.create_model(temporary_model)

        batch = []
        old_fields = [field for field in model._meta.local_concrete_fields if not field.primary_key]
        for record in model._base_manager.using(database).iterator(chunk_size=BATCH_SIZE):
            values = {field.attname: getattr(record, field.attname) for field in old_fields}
            batch.append(temporary_model(**values))

            if len(batch) == BATCH_SIZE:
                temporary_model._base_manager.using(database).bulk_create(
                    batch,
                    batch_size=BATCH_SIZE,
                )
                batch = []

        if batch:
            temporary_model._base_manager.using(database).bulk_create(
                batch,
                batch_size=BATCH_SIZE,
            )

        schema_editor.delete_model(model)
        schema_editor.alter_db_table(
            temporary_model,
            temp_table,
            model._meta.db_table,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_project"),
    ]

    operations = [
        migrations.RunPython(replace_integer_primary_keys_with_uuid),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="education",
                    name="id",
                    field=models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                migrations.AlterField(
                    model_name="language",
                    name="id",
                    field=models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                migrations.AlterField(
                    model_name="skillgroup",
                    name="id",
                    field=models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
    ]
