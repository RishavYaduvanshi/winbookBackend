
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notifzz", "0003_alter_notification_post"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"ordering": ["-date"]},
        ),
    ]
