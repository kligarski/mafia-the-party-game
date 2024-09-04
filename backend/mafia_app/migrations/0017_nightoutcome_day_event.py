# Generated by Django 5.0.7 on 2024-09-04 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafia_app', '0016_end_day_nightoutcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='nightoutcome',
            name='day_event',
            field=models.ForeignKey(default=84, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mafia_app.day'),
            preserve_default=False,
        ),
    ]
