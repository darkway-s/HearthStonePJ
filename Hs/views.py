from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import RegisterForm, KeywordForm
from Hs import models
from .models import SummonerClass, Keyword, Card


# Create your views here.


def index(request):
    return render(request, 'Hs/index.html', context={
        'welcome': '欢迎访问Kevin和Kass的炉石PJ首页'
    })


def index1(request):
    return render(request, 'Hs/index.html', context={
        'welcome': 'test1'
    })


def cards(request):
    sc_list = SummonerClass.objects.all()
    sc_sel = request.GET.get('sc_sel', default='')
    cost_sel = request.GET.get('cost_sl', default=1)
    cd_list = Card.objects.filter(cost=cost_sel)
    if sc_sel != '':
        cd_list = cd_list.filter(card_class=sc_sel)
    return render(request, 'Hs/cards.html', context={
        'class': '选择职业' if sc_sel == '' else sc_sel,
        'sc_sel': sc_sel,
        'sc_list': sc_list,
        'cost_sel': cost_sel,
        'cd_list': cd_list,
    })


def keyword_list(request):
    keyword = models.Keyword.objects.all()
    return render(request, 'Hs/keyword_list.html', {'keyword_list': keyword})


def keyword_add(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        # 判断表单值是否和法
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            keyword = Keyword(name=name, description=description)
            keyword.save()
            return redirect('/keyword_list')
    else:
        form = KeywordForm()
        return render(request, 'Hs/keyword_add.html', context={"form": form})


def keyword_edit(request):
    form = KeywordForm(request.POST)
    if request.method == 'POST':
        edit_name = request.GET.get('name')
        edit_obj = models.Keyword.objects.get(name=edit_name)
        edit_description = edit_obj.description

        form.name = edit_name
        form.description = edit_description
        edit_obj.save()
        return redirect('/keyword_list')

    else:

        edit_name = request.GET.get('name')
        edit_obj = models.Keyword.objects.get(name=edit_name)
        edit_description = edit_obj.description
        form = KeywordForm(
            initial={
                'name': edit_name,
                'description': edit_description,
            })

        return render(request, 'Hs/keyword_edit.html', context={"form": form})


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
