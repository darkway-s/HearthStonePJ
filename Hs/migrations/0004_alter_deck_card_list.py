# Generated by Django 3.2.3 on 2021-06-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hs', '0003_auto_20210610_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='card_list',
            field=models.ManyToManyField(null=True, through='Hs.DeckCard', to='Hs.Card'),
        ),
    ]