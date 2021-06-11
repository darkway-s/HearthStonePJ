from Hs import forms
from Hs.models import Card, SummonerClass, Keyword, RaceClass, SetClass


# 更新卡牌的关键词
def card_edit_keyword(sid, n_keyword):
    _card = Card.objects.get(id=sid)
    _card.keyword.set(n_keyword)
    _card.save()
    return _card


# 更新身材和费用
def card_edit_build(sid, n_cost, n_attack, n_health):
    _card = Card.objects.get(id=sid)
    _card.cost = n_cost
    _card.attack = n_attack
    _card.health = n_health
    _card.save()
    return _card


# 全部更新卡牌, n_card_class和n_keyword为list, html中可以用form获取, views中可以用getlist方法获取
def card(sid, n_name, n_type, n_rarity, n_set, n_card_class, n_collectible, n_keyword,
         n_cost, n_attack, n_health,
         n_description, n_background, n_race, n_img):
    _card = Card.objects.get(id=sid)
    _card.name = n_name
    _card.type = n_type
    _card.rarity = n_rarity
    _card.collectible = n_collectible
    _card.cost = n_cost
    _card.attack = n_attack
    _card.health = n_health
    _card.description = n_description
    _card.background = n_background
    if n_img is not None:
        _card.img = n_img

    # 外键更新
    _card.set_id = n_set
    _card.race_id = n_race
    # ManyToManyField更新
    _card.card_class.set(n_card_class)
    _card.keyword.set(n_keyword)
    _card.save()
    return _card


# 更新关键词, 输入要匹配的id， 要修改成的名字，要修改成的描述
def keyword(sid, sname, sdes):
    _keyword = Keyword.objects.get(id=sid)
    _keyword.name = sname
    _keyword.description = sdes
    _keyword.save()
    return _keyword


# 更新职业
def summonerclass(sid, sname, s_img):
    _summonerclass = SummonerClass.objects.get(id=sid)
    _summonerclass.name = sname
    _summonerclass.img = s_img
    _summonerclass.save()
    return _summonerclass


# 更新合集
def setclass(sid, sname):
    _setclass = SetClass.objects.get(id=sid)
    _setclass.name = sname
    _setclass.save()
    return _setclass


# 更新种族
def raceclass(sid, name):
    _raceclass = RaceClass.objects.get(id=sid)
    _raceclass.name = name
    _raceclass.save()
    return _raceclass
