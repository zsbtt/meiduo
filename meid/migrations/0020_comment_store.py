# Generated by Django 2.1.4 on 2019-09-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meid', '0019_auto_20190910_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='store',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
