# Generated by Django 2.1.4 on 2019-08-22 22:29

from django.db import migrations, models
import django.db.models.deletion
import meid.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('is_show', models.IntegerField(default=1)),
                ('sort', models.IntegerField(default=1)),
                ('type', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'banner',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Cate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('pid', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=1)),
                ('pic', models.CharField(max_length=255)),
                ('top_id', models.IntegerField(default=0)),
                ('is_recommend', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'cate',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, default=99999999.99, max_digits=10)),
                ('store', models.IntegerField(default=0)),
                ('lock_store', models.IntegerField(default=0)),
                ('pic', models.CharField(max_length=100)),
                ('descrip', models.CharField(max_length=50)),
                ('t_comment', models.IntegerField(default=0)),
                ('top_id', models.IntegerField(default=0)),
                ('sales', models.IntegerField(default=0)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meid.Cate')),
            ],
            options={
                'db_table': 'goods',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField(default='')),
                ('is_recommend', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'news',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Sadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_admin', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'sadmin',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_recommend', models.IntegerField(default=1)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meid.Cate')),
            ],
            options={
                'db_table': 'tags',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('passwd', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=50)),
                ('signator', models.CharField(max_length=100)),
                ('image', models.CharField(default='', max_length=255)),
                ('is_valide', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user',
            },
            bases=(meid.models.Base, models.Model),
        ),
        migrations.AddField(
            model_name='goods',
            name='tagid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meid.Tags'),
        ),
    ]
