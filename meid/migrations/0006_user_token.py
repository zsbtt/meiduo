# Generated by Django 2.1.4 on 2019-08-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meid', '0005_resource_role_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]