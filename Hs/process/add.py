from Hs import forms
from Hs.models import SummonerClass, Keyword, Card


# 增加关键字， 返回增加的关键字本身
def keyword(name, description):
    _keyword = Keyword.objects.create(name=name, description=description)
    return _keyword
