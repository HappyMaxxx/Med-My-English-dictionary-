# Generated by Django 4.2.16 on 2024-11-13 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('med', '0003_word_user_alter_word_example'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WordGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('words', models.ManyToManyField(blank=True, to='med.word')),
            ],
            options={
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='med_wordgro_name_2822a3_idx')],
            },
        ),
    ]