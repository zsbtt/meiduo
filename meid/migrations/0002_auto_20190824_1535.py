# Generated by Django 2.1.4 on 2019-08-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='pic',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='cate',
            name='pic',
            field=models.CharField(default='', max_length=255),
        ),
    ]
