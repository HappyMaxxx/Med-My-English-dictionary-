# Generated by Django 4.2.16 on 2024-11-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0013_alter_word_is_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]
