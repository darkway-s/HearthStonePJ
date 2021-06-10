from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SummonerClass, RaceClass, SetClass, Keyword, Card, User, UserCard


class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'rarity', 'set', 'cost']


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'date_joined',
                    'arc_dust']


admin.site.register(Card, CardAdmin)
admin.site.register(SummonerClass)
admin.site.register(RaceClass)
admin.site.register(SetClass)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserCard)
"""
admin.site.register(Deck)
admin.site.register(DeckCard)
"""
