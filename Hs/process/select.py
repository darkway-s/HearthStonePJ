from Hs.models import SummonerClass, Keyword, Card, SetClass, User, RaceClass, UserCard, Deck, DeckCard


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
    return match(SummonerClass, s_id)


# 仅获取第一个
def summonerclass_one(s_name='', *, sid=-1):
    return select1_one(SummonerClass, s_name, sid=sid)


# 严格筛选: 职业， 法力水晶， 费用， 卡牌id
def card_strict_type(s_type):
    _card_list = Card.objects.filter(type=s_type)
    return _card_list


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
    return user.collection


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


# 模糊名称搜索卡牌
def card_vague_name(s_name=''):
    _card_list = Card.objects.filter(name__contains=s_name)
    return _card_list


def card_vague_description(s_description=''):
    _card_list = Card.objects.filter(description__contains=s_description)
    return _card_list


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


# 搜索对应的UserCard关系，给出单个元素
def user_card_match(user, card):
    _object = UserCard.objects.get(user=user, card=card)
    return _object


# 搜索对应的DeckCard关系，给出单个元素
def deck_card_match(s_deck, card):
    _object = DeckCard.objects.get(deck=s_deck, card=card)
    return _object


# 返回一个deck
def deck_match(s_id):
    _deck = Deck.objects.get(id=s_id)
    return _deck


# 列出所有套牌
def deck_all():
    return select_all(Deck)


# 模糊搜索套牌名称并精确搜索id（如果有的话）
def deck(s_name='', *, sid):
    return select1(Deck, s_name, sid=sid)


# 输入deck，返回这个deck中的卡牌列表，以二元元组的形式返回(card, amount)第一个元素是Card类，第二个元素是int型（表示这张卡的数量）
def deck_card_list(s_deck):
    cards_in_deck = DeckCard.objects.filter(deck=s_deck)
    _card_list = []
    for obj in cards_in_deck:
        _tuple = (obj.card, obj.amount)
        _card_list.append(_tuple)
    return _card_list


# 计算s_deck中有哪些卡牌
def deck_count(s_deck):
    _card_list = deck(s_deck)
    cnt = 0
    for obj in _card_list:
        # 加上每个amount
        cnt += obj[1]
    return cnt
