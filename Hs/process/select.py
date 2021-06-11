from Hs.models import SummonerClass, Keyword, Card, SetClass, User, RaceClass, UserCard, DeckCard, Deck


# select 基类
def select_all(ObjectClass):
    _object_list = ObjectClass.objects.all()
    return _object_list


# 对于name 和 id 的筛选
def select1(ObjectClass, s_name='', *, sid=-1):
    if sid == -1:
        _object_list = ObjectClass.objects.filter(name__contains=s_name)
    else:
        _object_list = ObjectClass.objects.filter(name__contains=s_name, id__exact=sid)
    return _object_list


def select1_one(ObjectClass, s_name='', *, sid=-1):
    _object = select1(ObjectClass, s_name, sid=sid)[0]
    if _object:
        return _object
    else:
        return None


def match(ObjectClass, s_name):
    _object = ObjectClass.objects.get(name=s_name)
    return _object


def match_id(ObjectClass, s_id):
    _object = ObjectClass.objects.get(id=s_id)
    return _object


# 基类结束

# 获得整个关键词列表
def keyword_all():
    return select_all(Keyword)


# 获得关键词列表， 返回这个列表
def keyword(s_name='', *, sid=-1):
    return select1(Keyword, s_name, sid=sid)


# 根据关键词模糊搜索
def keyword_vague_name(s_name):
    _keyword_list = Keyword.objects.filter(name__contains=s_name)


def keyword_match(s_name):
    return match(Keyword, s_name)


def keyword_match_id(s_id):
    return match(Keyword, s_id)


# 仅获取第一个
def keyword_one(s_name='', *, sid=-1):
    return select1_one(Keyword, s_name, sid=sid)


# 获得整个职业列表
def summonerclass_all():
    return select_all(SummonerClass)


# 获得职业列表， 返回这个列表
def summonerclass(s_name='', *, sid=-1):
    return select1(SummonerClass, s_name, sid=sid)


def summonerclass_match(s_name):
    return match(SummonerClass, s_name)


def summonerclass_match_id(s_id):
    return match_id(SummonerClass, s_id)


# 仅获取第一个
def summonerclass_one(s_name='', *, sid=-1):
    return select1_one(SummonerClass, s_name, sid=sid)


# 严格筛选: 法力水晶， 费用， 卡牌id


# 严格匹配一组关键词, 配合keyword使用
def card_strict_keyword1(s_keyword):
    _card = Card.objects.get(keyword=s_keyword)
    return _card


# 输入关键词（部分）名字，模糊匹配对应卡，返回一个card_list
def card_strict_keyword2(s_name):
    _keyword = keyword(s_name)
    _card_list = card_strict_keyword1(s_name)
    return _card_list


def card_all():
    return select_all(Card)


def card_user(user):
    return user.collection.all()


# card_list 传入，在此基础上筛选
def card_strict(_card_list=card_all(), s_name='', s_id=-1, s_class_name='', s_cost=-1):
    if s_name != '':
        _card_list = _card_list.filter(name=s_name)

    if s_id != -1:
        _card_list = _card_list.filter(id=s_id)

    if s_cost != -1 and s_cost != 10:
        _card_list = _card_list.filter(cost=s_cost)

    elif s_cost == 10:
        _card_list = _card_list.filter(cost__gte=s_cost)

    if s_class_name != '':
        s_class = summonerclass_match(s_class_name)
        _card_list = _card_list.filter(card_class=s_class)

    return _card_list


# 测试筛选
def card_cost(s_cost):
    _card_list = Card.objects.filter(cost=s_cost)
    return _card_list


# 严格名称搜索卡牌
def card_match(s_name):
    return match(Card, s_name)


def card_match_id(s_id):
    return match_id(Card, s_id)


# 整体模糊搜索
def card_vague_search(search_word, card_list=card_all()):
    _set = Card.objects.none()
    # 因为关键词在description中都有，所以就不对keyword进行select了

    # 卡牌名模糊搜索
    set2 = card_vague_name(s_name=search_word, card_list=card_list)

    # 卡牌描述模糊搜索
    set3 = card_vague_description(s_description=search_word, card_list=card_list)

    # 种族精确搜索
    set4 = card_strict_race(s_race_name=search_word, card_list=card_list)

    # 类型精确搜索
    s_type = type_match(search_word)
    if s_type == -1:
        set5 = Card.objects.none()
    else:
        set5 = card_strict_type(s_type=s_type[0], card_list=card_list)

    # 稀有度精确搜索
    s_rarity = rarity_match(search_word)
    if s_rarity == -1:
        set6 = Card.objects.none()
    else:
        set6 = card_strict_rarity(s_rarity=s_rarity[0], card_list=card_list)

    _set = _set.distinct().union(set2, set3, set4, set5, set6)
    return _set


# 模糊名称搜索卡牌
def card_vague_name(s_name='', card_list=card_all()):
    _card_list = card_list.filter(name__contains=s_name)
    return _card_list


def card_vague_description(s_description='', card_list=card_all()):
    _card_list = card_list.filter(description__contains=s_description)
    return _card_list


def card_strict_race(s_race_name, card_list=card_all()):
    try:
        s_race = race_match(s_race_name)
        race_s_card_list = s_race.card_race.all()
        card_list = card_list.intersection(race_s_card_list)

        return card_list
    except RaceClass.DoesNotExist:
        return Card.objects.none()


# 找到对应type的所有卡牌，记住，这里s_type输入的是TYPE_CHOICE中元组的首个元素
def card_strict_type(s_type, card_list=card_all()):
    _card_list = card_list.filter(type=s_type)
    return _card_list


"""
TYPE_CHOICES = (
        ('minion', '随从'),
        ('weapon', '武器'),
        ('spell', '法术')
    )
"""


# 根据类型名字返回对应type
# 若没找到对应type，则返回-1
def type_match(s_name):
    print("s_name = " + s_name)
    for i in range(0, 3):
        if s_name == Card.TYPE_CHOICES[i][1]:
            return Card.TYPE_CHOICES[i]
    return -1


def card_strict_rarity(s_rarity, card_list=card_all()):
    _card_list = card_list.filter(rarity=s_rarity)
    return _card_list


"""
RARITY_CHOICE = (
        ('basic', '基本'),
        ('common', '普通'),
        ('rare', '稀有'),
        ('epic', '史诗'),
        ('legend', '传说')
    )
"""


# 根据稀有度名字返回对应type
# 若没找到对应type，则返回-1
def rarity_match(s_name):
    print("s_name = " + s_name)
    for i in range(0, 5):
        if s_name == Card.RARITY_CHOICE[i][1]:
            return Card.RARITY_CHOICE[i]
    return -1


# 搜索是否有匹配的合集名
def set_all():
    return select_all(SetClass)


def set_match(s_name):
    return match(SetClass, s_name)


def set_match_id(s_id):
    return match_id(SetClass, s_id)


def race_all():
    return select_all(RaceClass)


# 搜索是否有匹配的种族名字
def race_match(s_name):
    return match(RaceClass, s_name)


def race_match_id(s_id):
    return match_id(RaceClass, s_id)


# 输入user，返回这个user中的卡牌列表，以二元元组的形式返回(card, amount)第一个元素是Card类，第二个元素是int型（表示这张卡的数量）
def user_card_all(s_user: User):
    cards_in_user = UserCard.objects.filter(user=s_user)
    _card_list = []
    for obj in cards_in_user:
        _tuple = (obj.card, obj.amount)
        _card_list.append(_tuple)
    return _card_list


# 搜索对应的UserCard关系，给出单个元素
def user_card_match(user, card):
    _object = UserCard.objects.get(user=user, card=card)
    return _object


# 列出所有套牌
def deck_all():
    return select_all(Deck)


# 列出一个用户的所有套牌
def deck_all_of_user(cur_user):
    return cur_user.deck_owner.all()


# 模糊搜索套牌名称并精确搜索id（如果有的话）
def deck_vague_name(s_name='', *, sid):
    return select1(Deck, s_name, sid=sid)


# 搜索对应的DeckCard关系，给出单个元素
def deck_card_match(s_deck, card):
    _object = DeckCard.objects.get(deck=s_deck, card=card)
    return _object


# 返回一个deck
def deck_match_id(s_id):
    _deck = Deck.objects.get(id=s_id)
    return _deck


# 输入deck，返回这个deck中的卡牌列表，以二元元组的形式返回(card, amount)第一个元素是Card类，第二个元素是int型（表示这张卡的数量）
def deck_card_list(s_deck):
    cards_in_deck = DeckCard.objects.filter(deck=s_deck)
    _card_list = []
    for obj in cards_in_deck:
        _tuple = (obj.card, obj.amount)
        _card_list.append(_tuple)
    return _card_list


# 输入deck，user，返回这个deck可用职业的，并且在user卡牌收藏里的所有tuple
def deck_available_cards(obj_user: User, obj_deck):
    _cards_list = user_card_all(obj_user)
    obj_class = obj_deck.summoner_class
    _available_cards_list = []
    for _tuple in _cards_list:
        available_class = _tuple[0].card_class.all()
        neutral = summonerclass_match('中立')
        # 卡牌所在职业中包含该套牌的职业，或者是中立卡牌
        if obj_class in available_class or neutral in available_class:
            _available_cards_list.append(_tuple)
        else:
            # 否则什么也不做
            pass

    return _available_cards_list


# 计算s_deck中有哪些卡牌
def deck_count(s_deck):
    _card_list = deck_card_list(s_deck)
    cnt = 0
    for obj in _card_list:
        # 加上每个amount
        cnt += obj[1]
    return cnt


# 输入一个tuple(card, amount)，输出(card) 的list
def tuple2card(obj_tuple):
    return [val[0] for val in obj_tuple]


# 输入一个card_list, 输出用户拥有的这些卡牌的tuple(card, amount)
def card_list2user_tuple_list(card_list, obj_user):
    user_tuple = user_card_all(obj_user)
    user_cards = tuple2card(user_tuple)

    _tuple_list = []
    for _card in card_list:
        if _card in user_cards:
            # 如果用户拥有这张牌，那么显示这张牌和数量
            _obj = user_card_match(obj_user, _card)
            _tuple = (_card, _obj.amount)
            _tuple_list.append()


def user_all():
    return select_all(User)


def user_match_id(s_id):
    return match_id(User, s_id)
