# Generated by Django 2.1.4 on 2019-09-05 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meid', '0016_adress_is_se'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='good_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meid.Goods'),
            preserve_default=False,
        ),
    ]
