# Generated by Django 5.1.3 on 2024-12-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0020_readingtext_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingtext',
            name='is_auth_a',
            field=models.BooleanField(default=True),
        ),
    ]