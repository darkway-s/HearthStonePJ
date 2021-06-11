from django.urls import path, re_path, include
from django.views.static import serve
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cards', views.cards, name='cards'),
    path('search_cards', views.search_cards, name='search_cards'),

    path('keyword_list', views.keyword_list, name='keyword_list'),
    path('keyword_add', views.keyword_add, name='keyword_add'),
    re_path(r'^keyword_edit', views.keyword_edit, name='keyword_edit'),
    re_path(r'^keyword_drop', views.keyword_drop, name='keyword_drop'),

    re_path(r'^register', views.register, name='register'),

    path('manage', views.manage, name='manage'),
    path('manage/card/add', views.card_create, name='card_create'),
    path('test', views.test, name='test'),

    path('manage/card/add_sub', views.add_sub, name='add_sub'),
    path('manage/summonerclass_list', views.summonerclass_list, name='summonerclass_list'),
    path('manage/summonerclass_add', views.summonerclass_add, name='summonerclass_add'),
    path('manage/summonerclass_add_sub', views.summonerclass_add_sub, name='summonerclass_add_sub'),
    re_path(r'^summonerclass_edit', views.summonerclass_edit, name='summonerclass_edit'),
    re_path(r'^summonerclass_drop', views.summonerclass_drop, name='summonerclass_drop'),

    path('manage/raceclass_list', views.raceclass_list, name='raceclass_list'),
    # re_path(r'^raceclass_edit', views.raceclass_edit, name='raceclass_edit'),
    # re_path(r'^raceclass_drop', views.raceclass_drop, name='raceclass_edit'),
    path('manage/raceclass_add', views.raceclass_add, name='raceclass_add'),
    path('manage/raceclass_add_sub', views.raceclass_add_sub, name='raceclass_add_sub'),
    path('manage/keyword_list', views.keyword_list, name='keyword_list'),
    path('manage/keyword_add', views.keyword_add, name='keyword_add'),
    path('manage/keyword_add_sub', views.keyword_add_sub, name='keyword_add_sub'),
    path('manage/setclass_list', views.setclass_list, name='setclass_list'),
    path('manage/setclass_add', views.setclass_add, name='setclass_add'),
    path('manage/setclass_add_sub', views.setclass_list, name='setclass_add_sub'),
    path('manage/user_list', views.user_list, name='user_list'),
    path('manage/user_add', views.user_add, name='user_add'),
    path('manage/user_add_sub', views.user_add_sub, name='user_add_sub'),

    path('mycollection', views.mycollection, name='mycollection'),
    path('mycollection_comp', views.mycollection_comp, name='mycollection_comp'),
    path('mycollection_deck', views.mycollection_deck, name='mycollection_deck'),

    path('cd_comp', views.cd_comp, name='cd_comp'),
    path('cd_decomp', views.cd_decomp, name='cd_decomp'),

    path('dk_card_rem', views.dk_card_rem, name='dk_card_rem'),
    path('dk_card_add', views.dk_card_add, name='dk_card_add'),
    path('dk_new', views.dk_new, name='dk_new'),
    path('dk_new_sb', views.dk_new_sb, name='dk_new_sb'),
    path('dk_del', views.dk_del, name='dk_del'),
]
