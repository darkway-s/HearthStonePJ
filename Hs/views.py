from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, KeywordForm, SummonerClassForm
from Hs import models
from .models import SummonerClass
from .process import add, update, select



# Create your views here.


def index(request):
    return render(request, 'Hs/index.html', context={
        'welcome': '欢迎访问Kevin和Kass的炉石PJ首页'
    })


def cards(request):
    sc_list = select.summonerclass_all()
    sc_sel = request.GET.get('sc_sel', default='')
    cost_sel = request.GET.get('cost_sl', default='-1')
    cd_list = select.card_all()
    print('cost_sel=' + cost_sel)
    print('sc_sel=' + sc_sel)
    if cost_sel != '-1':
        cd_list = select.card_strict(_card_list=cd_list, s_cost=cost_sel)
    if sc_sel != '':
        cd_list = select.card_strict(_card_list=cd_list, s_class_name=sc_sel)
    return render(request, 'Hs/cards.html', context={
        'class': '选择职业' if sc_sel == '' else sc_sel,
        'sc_sel': sc_sel,
        'sc_list': sc_list,
        'cost_sel': cost_sel,
        'cd_list': cd_list,
    })


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
    if request.method == "POST":
        form = SummonerClassForm(request.POST)
        # 判断表单值是否合法
        if form.is_valid():
            name = form.cleaned_data['name']
            summonerclass = SummonerClass(name=name)
            summonerclass.save()
            return redirect('/summonerclass_list')
    else:
        form = SummonerClassForm()
        return render(request, 'Hs/summonerclass_add.html', context={"form": form})


def summonerclass_edit(request):
    if request.method == 'POST':
        form = SummonerClassForm(request.POST)
        edit_id = request.GET.get('id')
        try:
            if form.is_valid():
                edit_obj = models.SummonerClass.objects.get(id=edit_id)
                edit_obj.name = form.cleaned_data['name']
                edit_obj.save()
                return redirect('/summonerclass_list')
        except models.Keyword.DoesNotExist:
            edit_obj = None
            return redirect('/summonerclass_list')

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
    return redirect('/summonerclass_list')


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
    cd_list = select.card_all()
    return render(request, 'Hs/manage.html', context={
        'cd_list': cd_list,
    })


def card_create(request):
    return render(request, 'Hs/card_create.html', context={
    })



def test(request):
    obj = select.card_all()[0]
    print("该卡的稀有度为"+obj.rarity)
    return HttpResponse("Hello. It's a page for test.")
