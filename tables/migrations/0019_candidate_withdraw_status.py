# Generated by Django 3.1 on 2020-12-06 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0018_party_party_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='withdraw_status',
            field=models.IntegerField(default=0),
        ),
    ]
