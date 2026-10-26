from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_contactlead_options_contactlead_admin_notes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactlead",
            name="team_comment",
            field=models.TextField(
                blank=True,
                help_text="Comentarios del equipo sobre el estado del proyecto (visible en el portal).",
            ),
        ),
        migrations.AlterField(
            model_name="contactlead",
            name="admin_notes",
            field=models.TextField(
                blank=True,
                help_text="Notas internas solo para el equipo ALPRO (no visibles al cliente).",
            ),
        ),
        migrations.AlterField(
            model_name="contactlead",
            name="pending_summary",
            field=models.CharField(
                blank=True,
                help_text="Pendientes de pago o documentacion visibles al cliente.",
                max_length=255,
            ),
        ),
    ]
