from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, KeywordForm, SummonerClassForm
from Hs import models
from .models import SummonerClass, Card, UserCard, Deck
from .process import add, update, select, delete
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def index(request):
    return render(request, 'Hs/index.html', context={
        'welcome': '欢迎访问Kevin和Kass的炉石PJ首页'
    })


def cards(request):
    sc_list = select.summonerclass_all()
    cd_list = select.card_all()
    return render(request, 'Hs/cards.html', context={
        'sc_sel': '所有职业',
        'sc_list': sc_list,
        'cost_sel': -1,
        'cd_list': cd_list,
    })


@csrf_exempt
def search_cards(request):
    cd_list = select.card_all()
    sc_list = select.summonerclass_all()
    search_word = request.POST.get('search_word')
    sc_sel = request.POST.get('sc')
    cost_sel = request.POST.get('cst')

    if cost_sel != '-1':
        cd_list = select.card_strict(_card_list=cd_list, s_cost=cost_sel)
    if sc_sel != '所有职业':
        cd_list = select.card_strict(_card_list=cd_list, s_class_name=sc_sel)

    cd_list = select.card_vague_search(search_word, cd_list)

    return render(request, 'Hs/cards.html', context={
        'class': '选择职业' if sc_sel == '' else sc_sel,
        'sc_sel': sc_sel,
        'sc_list': sc_list,
        'cost_sel': cost_sel,
        'cd_list': cd_list,
        'search_word': search_word,
    })


def mycollection(request):
    try:
        tp_list = select.user_card_all(request.user)
    except:
        return render(request, 'Hs/mycollection.html', context={
            'pos': request.path,
        })
    cur_user = request.user
    dk_list = select.deck_all_of_user(cur_user)
    dtup_l = []
    for dk in dk_list:
        if select.deck_count(dk) < Deck.MAX_CARDS_IN_DECK:
            dtup_l.append((dk, '未完成'))
        else:
            dtup_l.append((dk, '已完成'))
    return render(request, 'Hs/mycollection.html', context={
        'tp_list': tp_list,
        'pos': request.get_full_path(),
        'dktup_list': dtup_l,
        'message': '',
    })


def mycollection_comp(request):
    cur_user = request.user
    all_card_list = select.card_all()
    # 每个_own_list 中的元素_own就是一个二元list，第一个元素是卡牌，第二个元素是数量
    _own_list = []
    for card in all_card_list:
        # 查询得到这个amount
        try:
            obj = select.user_card_match(cur_user, card)
            amount = obj.amount
        except UserCard.DoesNotExist:
            amount = 0
        _own = [card, amount]
        _own_list.append(_own)
        print(_own)
    dtup_l = []
    dk_list = select.deck_all_of_user(cur_user)
    for dk in dk_list:
        if select.deck_count(dk) < Deck.MAX_CARDS_IN_DECK:
            dtup_l.append((dk, '未完成'))
        else:
            dtup_l.append((dk, '已完成'))
    return render(request, 'Hs/mycollection.html', context={
        'tp_list': _own_list,
        'pos': request.get_full_path(),
        'dktup_list': dtup_l,
        'sc_list': select.summonerclass_all(),
    })


def mycollection_deck(request):
    try:
        tp_list = select.user_card_all(request.user)
    except:
        return render(request, 'Hs/mycollection_deck.html', context={
            'pos': request.get_full_path(),
        })
    try:
        cur_user = request.user
        dk_list = select.deck_all_of_user(cur_user)
        dk_card_list = []
        dk_sel_id = request.GET.get('dk_id', default='')
        if dk_sel_id != '':
            dk_sel = select.deck_match_id(dk_sel_id)
            tp_list = select.deck_available_cards(cur_user, dk_sel)
            dk_card_list = select.deck_card_list(dk_sel)
            for dk_card in dk_card_list:
                print(dk_card[0].name)
        dtup_l = []
        for dk in dk_list:
            if select.deck_count(dk) < Deck.MAX_CARDS_IN_DECK:
                dtup_l.append((dk, '未完成'))
            else:
                dtup_l.append((dk, '已完成'))
        return render(request, 'Hs/mycollection_deck.html', context={
            'tp_list': tp_list,
            'pos': request.get_full_path(),
            'dk_list': dk_list,
            'dktup_list': dtup_l,
            'dk_sel': select.deck_match_id(request.GET.get('dk_id')),
            'dk_card_list': dk_card_list,
            'message': ''
        })
    except models.Deck.DoesNotExist:
        return redirect('/mycollection')


def keyword_list(request):
    keyword = select.keyword_all()
    return render(request, 'Hs/keyword_list.html', {'keyword_list': keyword})


def keyword_add(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        # 判断表单值是否合法
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            add.keyword(name, description)
            return redirect('/keyword_list')
    else:
        form = KeywordForm()
        return render(request, 'Hs/keyword_add.html', context={"form": form})


def keyword_edit(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        edit_id = request.GET.get('id')
        try:
            if form.is_valid():
                sname = form.cleaned_data['name']
                sdes = form.cleaned_data['description']
                update.keyword(edit_id, sname, sdes)
                return redirect('/keyword_list')
        except models.Keyword.DoesNotExist:
            return redirect('/keyword_list')

    else:
        edit_id = request.GET.get('id')
        edit_obj = select.keyword_one(sid=edit_id)

        form = KeywordForm(
            initial={
                'name': edit_obj.name,
                'description': edit_obj.description,
            })

        return render(request, 'Hs/keyword_edit.html', context={
            "form": form,
            "id": edit_id
        })


def keyword_drop(request):
    drop_id = request.GET.get('id')
    drop_obj = select.keyword_one(sid=drop_id)
    drop_obj.delete()
    return redirect('/keyword_list')


def summonerclass_list(request):
    summonererclass = models.SummonerClass.objects.all()
    return render(request, 'Hs/summonerclass_list.html', {'summonerclass_list': summonererclass})


def summonerclass_add(request):
    return render(request, 'Hs/summonerclass_add.html', context={
    })


@csrf_exempt
def summonerclass_add_sub(request):
    request.encoding = 'utf-8'
    n_name = request.POST.get('n_name')
    n_img = request.FILES.get('n_img')
    add.summonerclass(n_name, n_img)
    return redirect('/manage/summonerclass_list')


def summonerclass_edit(request):
    if request.method == 'POST':
        form = SummonerClassForm(request.POST)
        edit_id = request.GET.get('id')
        try:
            if form.is_valid():
                edit_obj = models.SummonerClass.objects.get(id=edit_id)
                edit_obj.name = form.cleaned_data['name']
                edit_obj.save()
                return redirect('/manage/summonerclass_list')
        except models.Keyword.DoesNotExist:
            edit_obj = None
            return redirect('/manage/summonerclass_list')

    else:
        edit_id = request.GET.get('id')
        edit_obj = models.SummonerClass.objects.get(id=edit_id)

        form = SummonerClassForm(
            initial={
                'name': edit_obj.name,
            })

        return render(request, 'Hs/summonerclass_edit.html', context={
            "form": form,
            "id": edit_id
        })


def summonerclass_drop(request):
    drop_id = request.GET.get('id')
    drop_obj = models.SummonerClass.objects.get(id=drop_id)
    drop_obj.delete()
    return redirect('/manage/summonerclass_list')


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                # 注册成功，跳转回首页
                return redirect('/')

    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'Hs/register.html', context={'form': form})


def manage(request):
    sc_list = select.summonerclass_all()
    cd_list = select.card_all()
    return render(request, 'Hs/manage.html', context={
        'sc_sel': '所有职业',
        'sc_list': sc_list,
        'cost_sel': -1,
        'cd_list': cd_list,
    })


def card_create(request):
    tp_list = Card.TYPE_CHOICES
    rt_list = Card.RARITY_CHOICE
    st_list = select.set_all()
    sc_list = select.summonerclass_all()
    kw_list = select.keyword_all()
    rc_list = select.race_all()
    return render(request, 'Hs/card_create.html', context={
        'tp_list': tp_list,
        'rt_list': rt_list,
        'st_list': st_list,
        'sc_list': sc_list,
        'kw_list': kw_list,
        'rc_list': rc_list,
    })


"""
# 提供一个on/off值到True/False的转换
def on2true(bool_value):
    if bool_value == 'on':
        return True
    else:
        return False
"""


def card_edit(request):
    id = request.GET.get('id')
    cd = select.card_match_id(id)
    print(cd.name)
    print(cd.type)
    tp_list = Card.TYPE_CHOICES
    rt_list = Card.RARITY_CHOICE
    st_list = select.set_all()
    sc_list = select.summonerclass_all()
    kw_list = select.keyword_all()
    rc_list = select.race_all()
    return render(request, 'Hs/card_edit.html', context={
        'cd': cd,
        'tp_list': tp_list,
        'rt_list': rt_list,
        'st_list': st_list,
        'sc_list': sc_list,
        'kw_list': kw_list,
        'rc_list': rc_list,
    })


@csrf_exempt
def card_edit_sub(request):
    request.encoding = 'utf-8'
    n_name = request.POST.get('n_name')
    n_type = request.POST.get('n_type')
    n_rarity = request.POST.get('n_rarity')
    # 处理SetClass类
    n_set_id = request.POST.get('n_set')
    n_set = select.set_match_id(n_set_id)
    # 将checkbox的on/off值转换成True/False
    n_card_class = request.POST.getlist('n_card_class')

    collectible_str = request.POST.get('n_collectible')
    if collectible_str == "true":
        n_collectible = True
    else:
        n_collectible = False

    n_keyword = request.POST.getlist('n_keyword')

    n_cost = request.POST.get('n_cost')
    n_attack = request.POST.get('n_attack')
    n_health = request.POST.get('n_health')
    n_description = request.POST.get('n_description')
    n_background = request.POST.get('n_background')

    n_race_id = request.POST.get('n_race')
    n_race = select.race_match_id(n_race_id)

    n_img = request.FILES.get('n_img')
    update.card(request.GET.get('id'),
                n_name,
                n_type,
                n_rarity,
                n_set,
                n_card_class,
                n_collectible,
                n_keyword,
                n_cost,
                n_attack,
                n_health,
                n_description,
                n_background,
                n_race,
                n_img,
                )
    return redirect('/manage')


def card_drop(request):
    id = request.GET.get('id')
    delete.card(id)
    return redirect('/manage')


@csrf_exempt
def add_sub(request):
    request.encoding = 'utf-8'
    n_name = request.POST.get('n_name')
    n_type = request.POST.get('n_type')
    n_rarity = request.POST.get('n_rarity')
    # 处理SetClass类
    n_set_id = request.POST.get('n_set')
    n_set = select.set_match_id(n_set_id)
    # 将checkbox的on/off值转换成True/False
    n_card_class = request.POST.getlist('n_card_class')

    collectible_str = request.POST.get('n_collectible')
    if collectible_str == "true":
        n_collectible = True
    else:
        n_collectible = False

    n_keyword = request.POST.getlist('n_keyword')

    n_cost = request.POST.get('n_cost')
    n_attack = request.POST.get('n_attack')
    n_health = request.POST.get('n_health')
    n_description = request.POST.get('n_description')
    n_background = request.POST.get('n_background')

    n_race_id = request.POST.get('n_race')
    n_race = select.race_match_id(n_race_id)

    n_img = request.FILES.get('n_img')
    print(n_img)
    add.card(n_name,
             n_type,
             n_rarity,
             n_set,
             n_card_class,
             n_collectible,
             n_keyword,
             n_cost,
             n_attack,
             n_health,
             n_description,
             n_background,
             n_race,
             n_img,
             )
    return redirect('/manage')


def raceclass_list(request):
    rc_list = select.race_all()
    return render(request, 'Hs/race_list.html', {
        'rc_list': rc_list
    })


def raceclass_add(request):
    return render(request, 'Hs/race_add.html', context={
    })


def raceclass_edit(request):
    race_id = request.GET.get('id')
    rc = select.race_match_id(race_id)
    return render(request, 'Hs/race_edit.html', context={
        'rc': rc,
    })


@csrf_exempt
def raceclass_edit_sub(request):
    race_id = request.GET.get('id')
    rc_name = request.POST.get('rc_name')
    update.raceclass(race_id, rc_name)
    return redirect('/manage/raceclass_list')


def raceclass_drop(request):
    race_id = request.GET.get('id')
    delete.raceclass(race_id)
    return redirect('/manage/raceclass_list')


@csrf_exempt
def raceclass_add_sub(request):
    n_name = request.POST.get('n_name')
    add.raceclass(n_name)
    return redirect('/manage/raceclass_list')


def setclass_list(request):
    st_list = select.set_all()
    return render(request, 'Hs/setclass_list.html', context={
        'st_list': st_list
    })


def setclass_edit(request):
    set_id = request.GET.get('id')
    st = select.set_match_id(set_id)
    return render(request, 'Hs/setclass_edit.html', context={
        'st': st,
    })


def setclass_edit_sub(request):
    id = request.GET.get('id')
    n_name = request.POST.get('n_name')
    update.setclass(id, n_name)
    return redirect('/manage/setclass_list')


def setclass_add(request):
    return render(request, 'Hs/setclass_add.html', context={
    })


@csrf_exempt
def setclass_add_sub(request):
    n_name = request.POST.get('n_name')
    add.setclass(n_name)
    return redirect('/manage/setclass_list')


def setclass_drop(request):
    set_id = request.GET.get('id')
    delete.setclass(set_id)
    return redirect('/manage/setclass_list')


def user_list(request):
    us_list = select.user_all()
    return render(request, 'Hs/user_list.html', context={
        'us_list': us_list
    })


def user_add(request):
    id = request.GET.get('id')
    us_add = select.user_match_id(id)
    update.arc_up(us_add, 1000)
    return redirect('/manage/user_list')


def user_add_sub(request):
    return render(request, 'Hs/card_create.html', context={
    })


def keyword_add_sub(request):
    return render(request, 'Hs/card_create.html', context={
    })


# 卡牌制作
def cd_comp(request):
    cur_user = request.user
    s_card_id = request.GET.get('c_id')
    s_card = select.card_match_id(s_card_id)
    # 返回值
    ret = add.collection_one(cur_user, s_card)
    if ret == -1:
        # 奥术之尘不足
        message = '奥术之尘不足'
    elif ret == -2:
        # 当前卡牌数大于等于2张，无法合成
        message = '已拥有超过两张卡牌，无法继续合成'
    else:
        # 正常合成
        arc_cost = ret.card.compose_price()
        message = '合成成功，消耗了' + str(arc_cost) + '奥术之尘'
    return render(request, 'Hs/message.html', context={
        'pos': request.GET.get('pos'),
        'message': message,
    })


# 卡牌分解
def cd_decomp(request):
    cur_user = request.user
    s_card_id = request.GET.get('c_id')
    s_card = select.card_match_id(s_card_id)
    del_ret = delete.collection_one(cur_user, s_card)
    if del_ret == -1:
        message = '分解后会使您的套牌卡牌数量不足，请从套牌中删除后再分解。'
    else:
        message = '分解成功，获得了' + str(del_ret) + '点奥术之尘'
    return render(request, 'Hs/message.html', context={
        'pos': request.GET.get('pos'),
        'message': message,
    })


def dk_card_rem(request):
    dk_sel_id = request.GET.get('dk_id')
    cd_sel_id = request.GET.get('cd_id')
    dk_sel = select.deck_match_id(dk_sel_id)
    cd_sel = select.card_match_id(cd_sel_id)
    delete.deck_card_one(dk_sel, cd_sel)
    return redirect('/mycollection_deck?dk_id=' + request.GET.get('dk_id'))


def dk_card_add(request):
    dk_sel_id = request.GET.get('dk_id')
    cd_sel_id = request.GET.get('c_id')
    dk_sel = select.deck_match_id(dk_sel_id)
    cd_sel = select.card_match_id(cd_sel_id)
    message = add.deck_append(dk_sel, cd_sel)
    return redirect('/mycollection_deck?dk_id=' + request.GET.get('dk_id'))


def dk_new(request):
    cur_user = request.user
    dk_list = select.deck_all_of_user(cur_user)
    sc_list = select.summonerclass_all()
    sc_list = sc_list.exclude(name='中立')
    print(sc_list)
    dtup_l = []
    for dk in dk_list:
        if select.deck_count(dk) < Deck.MAX_CARDS_IN_DECK:
            dtup_l.append((dk, '未完成'))
        else:
            dtup_l.append((dk, '已完成'))
    return render(request, 'Hs/mycollection_new_deck.html', context={
        'sc_list': sc_list,
        'dk_list': dk_list,
        'dktup_list': dtup_l,
        'pos': request.get_full_path(),
    })


@csrf_exempt
def dk_new_sb(request):
    n_name = request.POST.get('n_name')
    n_sc = request.POST.get('n_sc')
    print(n_sc)
    sc = select.summonerclass_match_id(n_sc)
    add.deck_null(request.user, n_name, sc)
    return redirect('/dk_new')


def dk_del(request):
    dk_id = request.GET.get('dk_id')
    dk = select.deck_match_id(dk_id)
    delete.deck(dk)
    return redirect(request.GET.get('pos'))


def test(request):
    obj = select.card_all()[0]
    print("该卡的稀有度为" + obj.rarity)
    return HttpResponse("Hello. It's a page for test.")
