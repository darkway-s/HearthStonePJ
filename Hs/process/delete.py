from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass
from . import select


# 删除关键字
def keyword(sid):
    _keyword = Keyword.objects.get(id=sid)
    _keyword.delete()
    return None

"""
# 删除卡牌
# 给拥有该卡牌的角色全额返尘
def card(sid):
    _card = Card.objects.get(id=sid)
    # 拥有过这张卡的玩家
    owner_list = _card.collection_set.all()
    for owner in owner_list:
        collection_one(owner, _card)
    _card.delete()
    return None
"""

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

"""
# 分解卡牌, 输入user类，卡牌类
def collection_one(cur_user, s_card):
    def decompose(user_card_obj, obj_card, obj_user):
        price = obj_card.decompose_price
        user_card_obj.amount -= 1
        user_card_obj.save()
        # 无卡牌收藏则删除
        if user_card_obj.amount == 0:
            user_card_obj.delete()

        obj_user.arc_dust += price
        obj_user.save()

    try:
        _object = select.user_card_match(cur_user, s_card)
        decompose(_object, s_card, cur_user)
        print("正常分解")
        return True

    except UserCard.DoesNotExist:
        # 一张也没，注意，实际运行中这种情况不应触发！前端不应该给没有这张卡的人显示分解按钮
        print("你没有这张卡牌")
        return False
"""