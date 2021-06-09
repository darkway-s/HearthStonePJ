from Hs.process import select
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


# 增加某一张卡牌中的关键字, 输入Card类和Keyword类
def card_keyword_append(s_card, s_keyword):
    s_card.keyword.add(s_keyword)


# 增加某一张卡牌中的关键字, 输入Card类和Keyword的名字
def card_keyword_append2(s_card, s_keyword_name):
    s_keyword = select.keyword_match(s_keyword_name)
    card_keyword_append(s_card, s_keyword)


# 增加关键字类， 返回增加的关键字本身
def keyword(name, description):
    try:
        in_keyword = select.keyword_match(name)
        print("重复关键词类%s " % in_keyword.name)
        return in_keyword
    except Keyword.DoesNotExist:
        _keyword = Keyword.objects.create(name=name, description=description)
        return _keyword


# 增加职业， 返回本身
def summonerclass(name):
    try:
        in_obj = select.summonerclass_match(name)
        print("重复职业类%s " % in_obj.name)
        return in_obj
    except SummonerClass.DoesNotExist:
        _summonerclass = SummonerClass.objects.create(name=name)
        return _summonerclass


# 增加合集
def setclass(name):
    try:
        in_obj = select.set_match(name)
        print("重复职业类%s " % in_obj.name)
        return in_obj
    except SetClass.DoesNotExist:
        _setclass = SetClass.objects.create(name=name)
        return _setclass


# 增加种族
def raceclass(name):
    try:
        in_obj = select.race_match(name)
        print("重复种族类%s " % in_obj.name)
        return in_obj
    except RaceClass.DoesNotExist:
        _raceclass = RaceClass.objects.create(name=name)
        return _raceclass


# 增加卡牌收藏, 输入user类，卡牌类
def collection(cur_user, s_card):
    cur_user.collection.add(s_card)
    return
    pass
