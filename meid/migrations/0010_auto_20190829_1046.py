# Generated by Django 2.1.4 on 2019-08-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meid', '0009_auto_20190828_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_valide',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.IntegerField(default=0),
        ),
    ]
