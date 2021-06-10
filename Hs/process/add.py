from Hs.process import select
from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass, UserCard, Deck, DeckCard


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


# 创建一个空的套牌, 输入为用户, 套牌名字, 职业列表
def deck_null(owner, name, summoner_class):
    new_deck = Deck.objects.create(name=name, summoner_class=summoner_class, owner=owner)
    return new_deck


# 在目标套牌中增加目标卡牌
# 对于这种情况进行讨论，用户只有一张卡A，但是套牌中已经添加一张卡A了，这时应该拒绝再放入卡A
def deck_append(obj_deck: Deck, obj_card: Card):
    if select.deck_count(obj_deck) >= Deck.MAX_CARDS_IN_DECK:
        print("套牌中已经有太多卡了")
        return "套牌中已经有太多卡了"
    try:
        # 判断套牌中是否已经有了这张卡牌
        _object = select.deck_card_match(obj_deck, obj_card)
        # 判断用户是否拥有足够的卡牌， 如果只有一张牌，并且套牌中已经有一张了，那就报错
        obj_user = obj_deck.owner
        obj_user_card = select.user_card_match(obj_user, obj_card)
        own_amount = obj_user_card.amount
        if own_amount == 1:
            print("你只有一张%s" % obj_card)
            return "你只有一张%s" % obj_card

        if _object.amount >= 2:
            print("套牌中已有超过两张该卡牌，无法继续添加！")
            return "套牌中已有超过两张该卡牌，无法继续添加！"
        else:
            # 只有一张
            _object.amount += 1
            _object.save()
            print("成功添加第二张%s" % _object.card.name)
            return "成功添加第二张%s" % _object.card.name
    except DeckCard.DoesNotExist:
        # 一张也没
        new_obj = DeckCard.objects.create(deck=obj_deck, card=obj_card, amount=1)
        print("成功添加第一张%s" % new_obj.card.name)
        return "成功添加第一张%s" % new_obj.card.name


# 合成卡牌, 输入user类，卡牌类
# 根据当前拥有的这张卡牌的数量（0,1,2）
# 0张会进行合成，在UserCard关系里新增
# 1张会在UserCard对应行增加一个amount
# 2张以上则拒绝合成。
# 然后再判断用户当前奥术之尘与卡牌合成价格相比是否足够，如果够才会合成并扣除相应的奥术之尘
# 如果合成成功，则返回合成的UserCard，如果因为奥术之尘不够而失败，则返回-1，如果因为当前卡牌拥有量已经大于等于2，则返回-2
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
            print("你没有足够的奥术之尘")
            return -1

    # 开始
    try:
        _object = select.user_card_match(cur_user, s_card)
        if _object.amount >= 2:
            print("已拥有超过两张卡牌，无法继续合成！")
            return -2
        else:
            # 只有一张
            price = s_card.compose_price()
            if cur_user.arc_dust >= price:
                cur_user.arc_dust -= price
                cur_user.save()
                _object.amount += 1
                _object.save()
                return _object
            else:
                print("%s没有足够的奥术之尘" % cur_user.name)
                return -1

    except UserCard.DoesNotExist:
        # 一张也没
        ret = compose(cur_user, s_card)
        print("合成第一张")
        return ret
