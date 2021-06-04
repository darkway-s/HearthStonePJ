from Hs import forms
from Hs.models import SummonerClass, Keyword, Card


# 更新关键词, 输入要匹配的id， 要修改成的名字，要修改成的描述
def keyword(sid, sname, sdes):
    _keyword = Keyword.objects.get(id=sid)
    _keyword.name = sname
    _keyword.description = sdes
    _keyword.save()
    return _keyword
