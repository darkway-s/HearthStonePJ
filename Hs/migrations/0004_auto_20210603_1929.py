# Generated by Django 3.2.3 on 2021-06-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hs', '0003_alter_card_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='关键词id'),
        ),
        migrations.AlterField(
            model_name='raceclass',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='种族id'),
        ),
        migrations.AlterField(
            model_name='setclass',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='合集id'),
        ),
        migrations.AlterField(
            model_name='summonerclass',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='职业id'),
        ),
    ]