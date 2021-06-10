from Hs.process import select
from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass, UserCard


# 增加卡牌, n_card_class和n_keyword为list, html中可以用form获取, views中可以用getlist方法获取
def card(n_name, n_type, n_rarity, n_set, n_card_class, n_collectible, n_keyword, n_cost, n_attack, n_health,
         n_description, n_background, n_race, n_img):
    _card = Card.objects.create(name=n_name, type=n_type,
                                rarity=n_rarity, set=n_set,
                                collectible=n_collectible, race=n_race,
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
def summonerclass(s_name, s_img):
    try:
        in_obj = select.summonerclass_match(s_name)
        print("重复职业类%s " % in_obj.name)
        return in_obj
    except SummonerClass.DoesNotExist:
        _summonerclass = SummonerClass.objects.create(name=s_name, img=s_img)
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


"""
# 创建一个空的套牌, 输入为套牌名字
def deck_null(name, summoner_class):
    new_deck = Deck.objects.create(name=name, summoner_class=summoner_class)
    return new_deck


# 在目标套牌中增加目标卡牌
def deck_append(obj_deck, obj_card):
    if select.deck_count(obj_deck) > Deck.MAX_CARDS_IN_DECK:
        print("套牌中已经有太多卡了")
        return False

    try:
        _object = select.deck_card_match(obj_deck, obj_card)
        if _object.amount >= 2:
            print("套牌中已有超过两张卡牌，无法继续添加！")
            return 2
        else:
            # 只有一张
            _object.amount += 1
            _object.save()
            print("添加第二张%s" % _object.card.name)
            return 1
    except DeckCard.DoesNotExist:
        # 一张也没
        new_obj = DeckCard.objects.create(deck=obj_deck, card=obj_card, amount=1)
        print("添加第一张%s" % new_obj.card.name)
        return new_obj


# 合成卡牌, 输入user类，卡牌类
# 根据当前拥有的这张卡牌的数量（0,1,2）
# 0张会进行合成，在UserCard关系里新增
# 1张会在UserCard对应行增加一个amount
# 2张以上则拒绝合成。
# 然后再判断用户当前奥术之尘与卡牌合成价格相比是否足够，如果够才会合成并扣除相应的奥术之尘
def collection_one(cur_user, s_card):
    def compose(obj_user, obj_card):
        obj_price = obj_card.compose_price()
        print("obj_price = " + str(obj_price))

        if obj_user.arc_dust >= obj_price:
            obj_user.arc_dust -= obj_price
            obj_user.save()
            new_collect = UserCard.objects.create(user=obj_user, card=obj_card, amount=1)
            return new_collect
        else:
            print("%s没有足够的奥术之尘" % obj_user.name)
            return False

    # 开始
    try:
        _object = select.user_card_match(cur_user, s_card)
        if _object.amount >= 2:
            print("已拥有超过两张卡牌，无法继续合成！")
            return 2
        else:
            # 只有一张
            price = s_card.compose_price()
            if cur_user.arc_dust >= price:
                cur_user.arc_dust -= price
                cur_user.save()
                _object.amount += 1
                _object.save()
                return 1
            else:
                print("%s没有足够的奥术之尘" % cur_user.name)
                return False

    except UserCard.DoesNotExist:
        # 一张也没
        compose(cur_user, s_card)
        print("合成第一张")
"""
