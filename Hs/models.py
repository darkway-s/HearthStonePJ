from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


# Create your models here.


# 职业列表
class SummonerClass(models.Model):
    id = models.AutoField('职业id', primary_key=True)
    name = models.CharField('职业名称', max_length=10, unique=True)

    class Meta:
        verbose_name = '职业列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 种族
class RaceClass(models.Model):
    id = models.AutoField('种族id', primary_key=True)
    name = models.CharField('种族名称', max_length=10, unique=True)

    class Meta:
        verbose_name = '种族列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 合集
class SetClass(models.Model):
    id = models.AutoField('合集id', primary_key=True)
    name = models.CharField('所属合集', max_length=64, unique=True)

    class Meta:
        verbose_name = '合集列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 关键词及其效果
class Keyword(models.Model):
    id = models.AutoField('关键词id', primary_key=True)
    name = models.CharField('关键词名称', max_length=64, unique=True)
    description = models.CharField('描述', max_length=64)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 卡牌类
class Card(models.Model):
    id = models.AutoField('卡牌id', primary_key=True)
    name = models.CharField('卡牌名', max_length=64, blank=True, default='')

    # 类型三选一: spell, minion, weapon
    TYPE_CHOICES = (
        ('minion', '随从'),
        ('weapon', '武器'),
        ('spell', '法术')
    )

    type = models.CharField('类型', max_length=10, choices=TYPE_CHOICES, default='minion')

    # 稀有度
    RARITY_CHOICE = (
        ('basic', '基本'),
        ('common', '普通'),
        ('rare', '稀有'),
        ('epic', '史诗'),
        ('legend', '传说')
    )
    rarity = models.CharField('稀有度', max_length=10, choices=RARITY_CHOICE, default='common')

    # 所属版本
    set = models.ForeignKey(SetClass, verbose_name='系列', on_delete=models.CASCADE, null=True, blank=True)
    # 这里隐含一个关系表
    # 每张卡牌属于的职业数量是不确定的
    # 有的是中立卡，所有职业可用。有的是三职业卡（暗金教），有的是双职业卡（通灵学院）
    # 默认为中立卡
    card_class = models.ManyToManyField(SummonerClass, verbose_name='可用职业')

    # 是否可以合成
    collectible = models.BooleanField('是否可以合成', default=1)

    # 允许没有关键词, 这里隐含一个关系表
    keyword = models.ManyToManyField(Keyword, verbose_name='关键词', null=True, blank=True)

    # 身材三项
    cost = models.IntegerField('费用', default=1)
    attack = models.IntegerField('攻击力', default=1)
    health = models.IntegerField('生命值', default=1)

    # 卡牌描述
    description = models.CharField('描述', max_length=100, blank=True)
    background = models.CharField('背景故事', max_length=200, blank=True)
    # 种族
    race = models.ForeignKey(RaceClass, verbose_name='种族', on_delete=models.SET_NULL, null=True, blank=True)

    # 图片
    img = models.ImageField('图片', upload_to='card_img', null=True, default='default.png')
    """
    # 以下是可选拓展
    # cost_to_craft
    # disenchanting_yield
    # artist
    # golden
    """

    def compose_price(self):
        COMPOSE_PRICE = {
            "basic": 0,
            "common": 40,
            "rare": 100,
            "epic": 400,
            "legend": 1600
        }
        return COMPOSE_PRICE[self.rarity]

    def decompose_price(self):
        DECOMPOSE_PRICE = {
            "basic": 0,
            "common": 5,
            "rare": 20,
            "epic": 100,
            "legend": 400
        }
        return DECOMPOSE_PRICE[self.rarity]

    class Meta:
        verbose_name = '卡牌'
        verbose_name_plural = verbose_name
        # 名字和图片的组合是唯一的
        constraints = [
            models.UniqueConstraint(fields=['name', 'img'], name='unique_card')
        ]

    def __str__(self):
        return self.name


class User(AbstractUser):
    # 覆写User，继承AbstractUser
    class Meta(AbstractUser.Meta):
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    # 【货币】金币，奥术之尘
    gold = models.BigIntegerField('金币', default=0)
    arc_dust = models.BigIntegerField('奥术之尘', default=0)

    # 默认is_superuser值为false
    def save(self, *args, **kwargs):
        self.is_superuser = False
        super().save(*args, **kwargs)


# 卡与用户的关系集
# 每个玩家的账户都对应一组卡牌收藏
class UserCard(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.CASCADE)
    card_list = models.ManyToManyField(Card, verbose_name='卡牌列表', null=True, blank=True)
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name = "卡牌收藏"
        verbose_name_plural = verbose_name

        # 卡牌收藏
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=0), name='collection_minimum')
        ]


class Test(models.Model):
    testword = models.CharField(max_length=10)
