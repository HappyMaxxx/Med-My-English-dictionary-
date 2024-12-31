# Generated by Django 5.1.3 on 2024-12-29 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0026_userprofile_charts_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('level', models.PositiveIntegerField()),
                ('icon', models.ImageField(blank=True, upload_to='achievements/')),
                ('ach_type', models.CharField(choices=[('1', 'Words'), ('2', 'Groups'), ('3', 'Friends'), ('4', 'Reading'), ('5', 'Interaction'), ('6', 'Content Quality'), ('7', 'Special')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='edited_words',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sent_groups',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='text_read',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='words_added_from_text',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_get', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='med.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time_get'],
                'indexes': [models.Index(fields=['-time_get'], name='med_userach_time_ge_249a42_idx')],
            },
        ),
    ]