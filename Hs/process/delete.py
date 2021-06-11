from Hs.models import SummonerClass, Keyword, Card, RaceClass, SetClass, UserCard, Deck, DeckCard
from . import select


# 删除关键字
def keyword(sid):
    _keyword = Keyword.objects.get(id=sid)
    _keyword.delete()
    return None


# 删除卡牌
# 给拥有该卡牌的角色全额返尘
def card(sid):
    _card = Card.objects.get(id=sid)
    # 拥有过这张卡的玩家
    owner_list = _card.usercard_set.all()
    for owner in owner_list:
        collection_one(owner, _card)
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


# 删除这个套牌中的一张卡（如果有两张，只会删除一张
def deck_card_one(obj_deck, obj_card):
    if select.deck_count(obj_deck) == 0:
        print("空套牌")
        return False
    try:
        _object = select.deck_card_match(obj_deck, obj_card)
        # 只有一张
        _object.amount -= 1
        _object.save()
        if _object.amount == 0:
            _object.delete()
            print("删除卡%s" % obj_card.name)
        else:
            print("删除一张%s" % _object.card.name)
        return 1
    except DeckCard.DoesNotExist:
        # 一张也没
        print("套牌中没有卡%s" % obj_card)
        return False


# 删除这个套牌，会自动级联删除对应的关系
def deck(s_deck):
    s_deck.delete()


# 分解卡牌, 输入user类，卡牌类
# 无这张卡牌则直接退出，有这张卡牌才会分解
# 分解后若已无这张卡牌，则会删除,
# 返回分解所得的奥术之尘数量
# 若分解后会导致用户套牌库中卡牌数量不足,则返回-1
def collection_one(cur_user, s_card):
    def decompose(user_card_obj, obj_card, obj_user):
        price = obj_card.decompose_price()
        user_card_obj.amount -= 1
        user_card_obj.save()
        obj_user.arc_dust += price
        obj_user.save()
        # 无卡牌收藏则删除
        if user_card_obj.amount == 0:
            user_card_obj.delete()
        return price

    _object_user_card = select.user_card_match(cur_user, s_card)
    # 对应tuple(card, amount)
    _object = (s_card, _object_user_card.amount)
    used_list = select.deck_used_card_list(cur_user)
    print("下面是分解一张卡牌的used_list")
    print(used_list)
    print(_object)

    # 可能存在危险
    # 以下情况有危险:
    # 1. 删除一张只有一张的卡牌，但是used_list中要用一张。处理：在deck中删除这张
    # 2. 删除一张有两张的卡牌，但是used_list中要用两张。处理：在deck中使得这张的数量-1

    if _object in used_list:
        if _object[1] == 1:
            print("删除该卡会导致部分套牌不可用!")
            return -1
        elif _object[1] == 2 and _object in used_list:
            print("删除该卡会导致部分套牌不可用!")
            return -1

    # 放心地删除
    appreciate = decompose(_object_user_card, s_card, cur_user)
    print("正常分解")
    return appreciate

    """
    except UserCard.DoesNotExist:
        # 一张也没，注意，实际运行中这种情况不应触发！前端不应该给没有这张卡的人显示分解按钮
        print("你没有这张卡牌")
        return -1
    """
