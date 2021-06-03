from django.urls import path, re_path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('1', views.index1, name='index1'),
    path('cards', views.cards, name='cards'),
    path('keyword_list', views.keyword_list, name='keyword_list'),
    path('keyword_add', views.keyword_add, name='keyword_add'),
    re_path(r'^register', views.register, name='register'),
]


