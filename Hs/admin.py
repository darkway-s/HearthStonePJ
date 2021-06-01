from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SummonerClass, RaceClass, SetClass, Keyword, Card, User


class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'rarity', 'set', 'cost']


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(Card, CardAdmin)
admin.site.register(SummonerClass)
admin.site.register(RaceClass)
admin.site.register(SetClass)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(User)
