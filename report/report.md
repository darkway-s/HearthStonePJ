# 实验报告

> 张驰一 19307130043 张开元 19307130227



# 一、实验题目

### 实验题目：

炉石传说卡牌库系统

### 实验背景：

一套**卡牌库**系统对卡牌的制造、删除、更新、搜索等方面进行统一管理，同时需要对每个玩家的**个人收藏**中卡牌的合成、分解进行管理，同时需要对每个玩家的所有**套牌**进行管理，可以向套牌中添加自己收藏中的卡牌。

除了在游戏（炉石传说）内，用户应当能在该网站上浏览到所有的卡牌及其详细信息，并且模拟游戏内对**个人收藏**的管理。



我们二人都是炉石传说的忠实玩家，选定这个题目的初衷是想模拟实现这个系统。未来如果有可能的话，完成网站布局，能够得到官方数据的授权，为不方便登录游戏的时候提供一个更轻量化的卡牌管理视图。



# 二、开发环境

> (操作系统，数据库管理软件，编程语言，客户端或web开发环境)

在`windows10`上进行开发，

使用`django`自带的`admin`进行数据库管理(version==3.2.3)，Navitcat进行辅助

数据库选用`SQLite`

编程语言为python(version==3.9)

web开发环境

# 三、数据库设计

## 模型设计

整个数据库共11个表，围绕Card表展开。

首先是**实体集**：

### SummonerClass职业

> 鉴于暴雪（炉石传说所属公司）有过加入新职业的操作（外域版本的恶魔猎手），并且有谣言称今年年要加入武僧，所以把职业单独做成一个可增改的类

id int：主键，自增

name char：名称，Unique约束

img file：图标



### RaceClass种族

id int：主键，自增

name char：名称，Unique约束



### SetClass合集

id int：主键，自增

name char：名称，Unique约束



### Keyword关键词

id int：主键，自增

name char：名称，Unique约束

description char：描述



### Card卡牌

id int: 主键，自增

name char：名称

type enum：卡牌类型，分为'随从'，'武器'，'法术'三类

rarity enum：稀有度，分为'基本'、'普通'、'稀有'、'史诗'、'传说'五类

collectible boolean：是否可合成

cost int：费用

attack int：攻击力

health int：生命值

description char：卡牌描述

background char：卡牌背景

img file：卡牌图片



set(set_id)：外键约束to Set，卡牌所属合集，实质上存储set的id，为int型

race(race_id)：外键约束to Race，卡牌的种族，允许为空



### User用户

> 继承自`django.contrib.auth.models.AbstractUser`，以下只说用到的类型

id int：主键

username char：名称，Unique约束，必填，长度为150个字符或以下

password char：密码，用`pbkdf2_sha256`加密后的密文存储在数据库中。

is_stuff boolean：是否为工作人员



arc_dust BigInt：奥术之尘数量（卡牌合成与分解所用到的货币），默认初始化为0



### Deck套牌

> 类内部存在变量MAX_CARDS_IN_DECK，作为规定每张套牌的上限

id int：主键，自增

name char：名称

owner(user_id)：外键约束to User，串联删除与更新



然后是**关系集**：

### class_card卡牌所属职业

> 这是一个多对一关系，因为多职业卡的存在，一张卡可能会对应多个职业。但是每张卡牌都必须有至少有一个职业。主键为这两个属性的并

SummonerClass_id int：职业

Card_id int：卡牌

### keyword_card卡牌中包含的关键词

> 这是一个多对多关系，因为多职业卡的存在，一张卡可能会对应多个职业。一张卡不一定有一个关键词，主键为这两个属性的并

Keywords_id int：职业

Card_id int：卡牌



### UserCard用户拥有的卡牌

> 这是一个多对多关系，主键为(User_id, Card_id)

User_id：用户

Card_id：卡牌

amount：卡牌数量， check(amount >= 0) as collection_minimum



### DeckCard套牌内的卡牌

> 这是一个多对多关系，主键为(User_id, Card_id)

Deck_id：套牌

Card_id：卡牌

amount：卡牌数量， check(amount >= 0) as collection_minimum



下面是数据库的**E-R图**：



![image-20210611213424122](image-20210611213424122.png)

## 视图、触发器与过程

> 由于django的性质，以上用python文件实现
>
> 在`Hs/process`下的`select.py,add.py,update.py,delete.py`中实现了很多，这里仅作举例

视图举例：

模糊搜索卡牌的相关属性，返回一个`<QuerySet>` （相关函数见源码`Hs/process/select.py`）

```python
# 整体模糊搜索
def card_vague_search(search_word, card_list=card_all()):
    _set = Card.objects.none()
    # 因为关键词在description中都有，所以就不对keyword进行select了

    # 卡牌名模糊搜索
    set2 = card_vague_name(s_name=search_word, card_list=card_list)

    # 卡牌描述模糊搜索
    set3 = card_vague_description(s_description=search_word, card_list=card_list)

    # 种族精确搜索
    set4 = card_strict_race(s_race_name=search_word, card_list=card_list)

    # 类型精确搜索
    s_type = type_match(search_word)
    if s_type == -1:
        set5 = Card.objects.none()
    else:
        set5 = card_strict_type(s_type=s_type[0], card_list=card_list)

    # 稀有度精确搜索
    s_rarity = rarity_match(search_word)
    if s_rarity == -1:
        set6 = Card.objects.none()
    else:
        set6 = card_strict_rarity(s_rarity=s_rarity[0], card_list=card_list)

    _set = _set.distinct().union(set2, set3, set4, set5, set6)
    return _set

```

触发器与过程举例：

```python
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
```



# 四、系统设计

### 密码加密存储：

Player1存储在数据库中的密码<img src="image-20210611203943669.png" alt="image-20210611203943669" style="zoom:50%;" /> 

### 用户注册：



输入密码“1”报错：<img src="image-20210611204431266.png" alt="image-20210611204431266" style="zoom:50%;" />

# 五、特色和创新点

# 六、实验分工

# 七、提交文件说明

# 八、实验总结

#### 张驰一：



#### 张开元：