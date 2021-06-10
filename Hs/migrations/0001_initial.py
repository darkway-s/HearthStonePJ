# Generated by Django 3.2.3 on 2021-06-10 13:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='卡牌id')),
                ('name', models.CharField(blank=True, default='', max_length=64, verbose_name='卡牌名')),
                ('type', models.CharField(choices=[('minion', '随从'), ('weapon', '武器'), ('spell', '法术')], default='minion', max_length=10, verbose_name='类型')),
                ('rarity', models.CharField(choices=[('basic', '基本'), ('common', '普通'), ('rare', '稀有'), ('epic', '史诗'), ('legend', '传说')], default='common', max_length=10, verbose_name='稀有度')),
                ('collectible', models.BooleanField(default=1, verbose_name='是否可以合成')),
                ('cost', models.IntegerField(default=1, verbose_name='费用')),
                ('attack', models.IntegerField(default=1, verbose_name='攻击力')),
                ('health', models.IntegerField(default=1, verbose_name='生命值')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='描述')),
                ('background', models.CharField(blank=True, max_length=200, verbose_name='背景故事')),
                ('img', models.ImageField(default='default.png', null=True, upload_to='card_img', verbose_name='图片')),
            ],
            options={
                'verbose_name': '卡牌',
                'verbose_name_plural': '卡牌',
            },
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='套牌id')),
                ('name', models.CharField(max_length=64, verbose_name='套牌名称')),
            ],
            options={
                'verbose_name': '套牌',
                'verbose_name_plural': '套牌',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='关键词id')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='关键词名称')),
                ('description', models.CharField(max_length=64, verbose_name='描述')),
            ],
            options={
                'verbose_name': '关键词',
                'verbose_name_plural': '关键词',
            },
        ),
        migrations.CreateModel(
            name='RaceClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='种族id')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='种族名称')),
            ],
            options={
                'verbose_name': '种族列表',
                'verbose_name_plural': '种族列表',
            },
        ),
        migrations.CreateModel(
            name='SetClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='合集id')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='所属合集')),
            ],
            options={
                'verbose_name': '合集列表',
                'verbose_name_plural': '合集列表',
            },
        ),
        migrations.CreateModel(
            name='SummonerClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='职业id')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='职业名称')),
                ('img', models.ImageField(default='default.png', null=True, upload_to='summonerclass_img', verbose_name='图片')),
            ],
            options={
                'verbose_name': '职业列表',
                'verbose_name_plural': '职业列表',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testword', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.card', verbose_name='卡牌')),
            ],
            options={
                'verbose_name': '卡牌收藏关系',
                'verbose_name_plural': '卡牌收藏关系',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gold', models.BigIntegerField(default=0, verbose_name='金币')),
                ('arc_dust', models.BigIntegerField(default=0, verbose_name='奥术之尘')),
                ('collections', models.ManyToManyField(through='Hs.UserCard', to='Hs.Card')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='usercard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.card', verbose_name='卡牌')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.deck', verbose_name='套牌')),
            ],
            options={
                'verbose_name': '套牌关系',
                'verbose_name_plural': '套牌关系',
            },
        ),
        migrations.AddField(
            model_name='deck',
            name='card_list',
            field=models.ManyToManyField(through='Hs.DeckCard', to='Hs.Card'),
        ),
        migrations.AddField(
            model_name='deck',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='拥有者'),
        ),
        migrations.AddField(
            model_name='deck',
            name='summoner_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hs.summonerclass', verbose_name='套牌职业'),
        ),
        migrations.AddField(
            model_name='card',
            name='card_class',
            field=models.ManyToManyField(to='Hs.SummonerClass', verbose_name='可用职业'),
        ),
        migrations.AddField(
            model_name='card',
            name='keyword',
            field=models.ManyToManyField(blank=True, null=True, to='Hs.Keyword', verbose_name='关键词'),
        ),
        migrations.AddField(
            model_name='card',
            name='race',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hs.raceclass', verbose_name='种族'),
        ),
        migrations.AddField(
            model_name='card',
            name='set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Hs.setclass', verbose_name='系列'),
        ),
        migrations.AddConstraint(
            model_name='usercard',
            constraint=models.CheckConstraint(check=models.Q(('amount__gte', 0)), name='collection_minimum'),
        ),
        migrations.AddConstraint(
            model_name='deckcard',
            constraint=models.CheckConstraint(check=models.Q(('amount__gte', 0)), name='card_minimum'),
        ),
        migrations.AddConstraint(
            model_name='card',
            constraint=models.UniqueConstraint(fields=('name', 'img'), name='unique_card'),
        ),
    ]
