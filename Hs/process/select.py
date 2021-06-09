from Hs import forms
from Hs.models import SummonerClass, Keyword, Card, SetClass


# 获得关键词列表， 返回这个列表
def keyword(s_name='', *, sid=-1):
    if sid == -1:
        _keyword_list = Keyword.objects.filter(name__contains=s_name)
    else:
        _keyword_list = Keyword.objects.filter(name__contains=s_name, id__exact=sid)
    return _keyword_list


def keyword_match(s_name):
    _keyword = Keyword.objects.get(name=s_name)
    return _keyword


# 仅获取第一个
def keyword_one(sname='', *, sid=-1):
    _keyword = keyword(sname, sid=sid)[0]
    if _keyword:
        return _keyword
    else:
        return None


# 获得关键词列表， 返回这个列表
def summonerclass(s_name='', *, sid=-1):
    if sid == -1:
        _summonerclass_list = SummonerClass.objects.filter(name__contains=s_name)
    else:
        _summonerclass_list = SummonerClass.objects.filter(name__contains=s_name, id__exact=sid)
    return _summonerclass_list


def summonerclass_match(s_name):
    _summonerclass = SummonerClass.objects.get(name=s_name)
    return _summonerclass


# 仅获取第一个
def summonerclass_one(sname='', *, sid=-1):
    _summonerclass = summonerclass(sname, sid=sid)[0]
    if _summonerclass:
        return _summonerclass
    else:
        return None


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
    _card_list = Card.objects.all()
    return _card_list


# card_list 传入，在此基础上筛选
def card_strict(_card_list=card_all(), s_name='', s_id=-1, s_class='', s_cost=-1):
    if s_name != '':
        _card_list = _card_list.filter(name=s_name)

    if s_id != -1:
        _card_list = _card_list.filter(id=s_id)

    if s_cost != -1 and s_cost != 10:
        _card_list = _card_list.filter(cost=s_cost)

    elif s_cost == 10:
        _card_list = _card_list.filter(cost__gte=s_cost)

    if s_class != '':
        _card_list = _card_list.filter(card_class=s_class)

    return _card_list


# 测试筛选
def card_cost(s_cost):
    _card_list = Card.objects.filter(cost=s_cost)
    return _card_list


# 模糊搜索卡牌
def card_vague_name(s_name=''):
    _card_list = Card.objects.filter(name__contains=s_name)
    return _card_list


def card_vague_description(s_description=''):
    _card_list = Card.objects.filter(description__contains=s_description)
    return _card_list


# 搜索是否有匹配的合集名
def set_match(s_name):
    _set = SetClass.objects.get(name=s_name)
    return _set


# 搜索是否有匹配的职业名字
def class_match(s_name):
    _class = SummonerClass.get(name=s_name)
    return _class
