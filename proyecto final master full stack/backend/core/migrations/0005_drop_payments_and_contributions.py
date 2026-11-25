from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_contactlead_verbose_labels"),
    ]

    operations = [
        migrations.DeleteModel(name="ClientContribution"),
        migrations.RemoveField(model_name="contactlead", name="payment_status"),
        migrations.RemoveField(model_name="contactlead", name="pending_summary"),
        migrations.RemoveField(model_name="contactlead", name="team_comment"),
    ]
