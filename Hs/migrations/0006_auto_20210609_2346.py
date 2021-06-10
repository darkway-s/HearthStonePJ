# Generated by Django 3.2.3 on 2021-06-09 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hs', '0005_delete_deck'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='套牌id')),
                ('name', models.CharField(max_length=64, verbose_name='套牌名称')),
            ],
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.card', verbose_name='卡牌')),
                ('s_deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.s_deck', verbose_name='套牌')),
            ],
            options={
                'verbose_name': '套牌',
                'verbose_name_plural': '套牌',
            },
        ),
        migrations.AddField(
            model_name='s_deck',
            name='card_list',
            field=models.ManyToManyField(through='Hs.DeckCard', to='Hs.Card'),
        ),
        migrations.AddConstraint(
            model_name='deckcard',
            constraint=models.CheckConstraint(check=models.Q(('amount__gte', 0)), name='card_minimum'),
        ),
    ]
