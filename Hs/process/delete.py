from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass


# 删除关键字
def keyword(sid):
    _keyword = Keyword.objects.get(id=sid)
    _keyword.delete()
    return None


# 删除卡牌
def card(sid):
    _card = Card.objects.get(id=sid)
    _card.delete()
    return None


def summonerclass(sid):
    _summonerclass = SummonerClass.objects.get(id=sid)
    _summonerclass.delete()
    return None


def setclass(sid):
    _setclass = SetClass.objects.get(id=sid)
    _setclass.delete()
    return None


def raceclass(sid):
    _raceclass = RaceClass.objects.get(id=sid)
    _raceclass.delete()
    return None
