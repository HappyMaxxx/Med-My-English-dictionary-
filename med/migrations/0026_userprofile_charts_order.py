# Generated by Django 5.1.3 on 2024-12-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0025_userprofile_show_bar_chart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='charts_order',
            field=models.CharField(default='Pie Chart,Bar Chart,Time Line', max_length=30),
        ),
    ]