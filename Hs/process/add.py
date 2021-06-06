from Hs import forms
from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass


# 增加卡牌, n_card_class和n_keyword为list, html中可以用form获取, views中可以用getlist方法获取
def card(n_name, n_type, n_rarity, n_set, n_card_class, n_collectible, n_keyword, n_cost, n_attack, n_health,
         n_description, n_background, n_race, n_img):
    _card = Card.objects.create(name=n_name, type=n_type,
                                rarity=n_rarity, set_id=n_set.id,
                                collectible=n_collectible, race_id=n_race.id,
                                cost=n_cost, attack=n_attack, health=n_health,
                                description=n_description, background=n_background,
                                img=n_img)
    # ManyToManyField添加
    _card.card_class.set(n_card_class)
    _card.keyword.set(n_keyword)
    _card.save()
    return _card


# 增加关键字， 返回增加的关键字本身
def keyword(name, description):
    _keyword = Keyword.objects.create(name=name, description=description)
    return _keyword


# 增加职业， 返回本身
def summonerclass(name):
    _summonerclass = SummonerClass.objects.create(name=name)
    return _summonerclass


# 增加合集
def setclass(name):
    _setclass = SetClass.objects.create(name=name)
    return _setclass


# 增加种族
def raceclass(name):
    _raceclass = RaceClass.objects.create(name=name)
