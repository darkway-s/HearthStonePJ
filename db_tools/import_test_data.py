# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
# 找到根目录（与工程名一样的文件夹）下的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hsproject.settings')

import django

django.setup()

# 引入的位置必须在这里，不可提前
from Hs.models import Set, Card, SummonerClass, Keyword, RaceClass, SetClass

from db_tools.data.cards_test1 import row_data
from Hs.process import add, select, update, delete

for card_detail in row_data:

    n_name = card_detail["name"]
    n_type = card_detail["type"].lower()
    n_rarity = card_detail["rarity"].lower()

    row_set_name = card_detail["set"]
    try:
        n_set = select.set_match(row_set_name)
    except Set.DoesNotExist:
        # 进行合集添加
        n_set = add.setclass(row_set_name)
        print("添加关键字(%s)" % 'row_set_name')

    row_class_name = card_detail["cardClass"]
    if isinstance(row_class_name, list):
        for row_name in row_class_name:
            try:
                n_card_class = select.class_match(row_name)
            except SummonerClass.DoesNotExist:
                n_card_class = add.summonerclass(row_name)
                print("新建职业(%s)" % 'row_name')
    else:
        try:
            n_card_class = select.class_match(row_class_name)
        except SummonerClass.DoesNotExist:
            n_card_class = add.summonerclass(row_class_name)
            print("新建职业(%s)" % 'row_class_name')

    n_collectible = card_detail["collectible"]

    if card_detail["mechanics"] is not None:
        row_keyword_name = card_detail["mechanics"]
        for row_name in row_keyword_name:
            try:
                n_keyword = select.keyword_match(row_name)
            except Keyword.DoesNotExist:
                n_keyword = add.keyword(row_name)
                print("新建关键字(%s)" % 'row_name')
    else:
        n_keyword = None

    n_cost = card_detail["cost"]
    n_attack = card_detail["attack"] if card_detail["attack"] is not None else 1
    n_health = card_detail["health"] if card_detail["health"] is not None else 1
    n_description = card_detail["text"]
    n_background = card_detail["flavor"]
    # TODO 种族这里还没引入
    # n_race = card_detail["race"]



    n_sale_price = float(int(card_detail["sale_price"].replace("￥", "").replace("元", "")))
    n_goods_brief = card_detail["desc"] if card_detail["desc"] is not None else ""
    n_goods_desc = card_detail["goods_desc"] if card_detail["goods_desc"] is not None else ""
    n_goods_front_image = card_detail["images"][0] if card_detail["images"] else ""

    card = Card(n_name, n_type, n_rarity, n_set, n_card_class,
                n_collectible, n_keyword, n_cost, n_attack, n_health,
                n_description, n_background, n_race, n_img)

    category_name = card_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        card.category = category[0]
    card.save()

    for goods_image in card_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.card = card
        goods_image_instance.save()
