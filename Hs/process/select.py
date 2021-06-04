from Hs import forms
from Hs.models import SummonerClass, Keyword, Card


# 获得关键词列表， 返回这个列表
def keyword(sname='', *, sid=-1):
    if sid == -1:
        _keyword_list = Keyword.objects.filter(name__contains=sname)
    else:
        _keyword_list = Keyword.objects.filter(id__exact=sid)
    return _keyword_list


# 仅获取第一个
def keyword_one(sname='', *, sid=-1):
    _keyword = keyword(sname, sid=sid)[0]
    if _keyword:
        return _keyword
    else:
        return None


# 严格筛选: 职业， 法力水晶， 费用， 卡牌id
def cards_strict(sname='', sid=-1, s_class='', s_cost=-1):
    _card_list = Card.objects.filter(name__contains=sname)

    if sid != -1:
        _card_list = _card_list.filter(id=sid)

    if s_cost != -1 & s_cost < 10:
        _card_list = _card_list.filter(cost=s_cost)

    elif s_cost == 10:
        _card_list = _card_list.filter(cost__gte=s_cost)

    if s_class != '':
        _card_list = _card_list.filter(card_class=s_class)

    return _card_list


# 测试筛选
def cards_cost(*s_cost):
    _card_list = Card.objects.filter(cost=s_cost)
    return _card_list
