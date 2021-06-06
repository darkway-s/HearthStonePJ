from Hs import forms
from Hs.models import SummonerClass, Keyword, Card


# 获得关键词列表， 返回这个列表
def keyword(s_name='', *, sid=-1):
    if sid == -1:
        _keyword_list = Keyword.objects.filter(name__contains=s_name)
    else:
        _keyword_list = Keyword.objects.filter(name__contains=s_name, id__exact=sid)
    return _keyword_list


# 仅获取第一个
def keyword_one(sname='', *, sid=-1):
    _keyword = keyword(sname, sid=sid)[0]
    if _keyword:
        return _keyword
    else:
        return None


# 严格筛选: 职业， 法力水晶， 费用， 卡牌id
def card_strict_type(s_type):
    _card_list = Card.objects.filter(type=s_type)


# 严格匹配一组关键词, 配合keyword使用
def card_strict_keyword1(s_keyword):
    _card = Card.objects.get(keyword=s_keyword)
    return _card


# 输入关键词（部分）名字，模糊匹配对应卡，返回一个card_list
def card_strict_keyword2(s_name):
    _keyword = keyword(s_name)
    _card_list = card_strict_keyword1(s_name)
    return _card_list


def card_strict(s_name='', s_id=-1, s_class='', s_cost=-1):
    _card_list = Card.objects.all()
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
