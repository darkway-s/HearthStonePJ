from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cards', views.cards, name='cards'),

    path('keyword_list', views.keyword_list, name='keyword_list'),
    path('keyword_add', views.keyword_add, name='keyword_add'),
    re_path(r'^keyword_edit', views.keyword_edit, name='keyword_edit'),
    re_path(r'^keyword_drop', views.keyword_drop, name='keyword_drop'),

    path('summonerclass_list', views.summonerclass_list, name='summonerclass_list'),
    path('summonerclass_add', views.summonerclass_add, name='summonerclass_add'),
    re_path(r'^summonerclass_edit', views.summonerclass_edit, name='summonerclass_edit'),
    re_path(r'^summonerclass_drop', views.summonerclass_drop, name='summonerclass_drop'),

    re_path(r'^register', views.register, name='register'),
]
