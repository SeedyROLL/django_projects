from django.contrib import admin
from mkt.models import Ad, Comment, Fav

class FavAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user') # Показывает заголовок объявления и имя пользователя в таблице
    list_filter = ('user',)       # Добавляет фильтр по пользователям справа

admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(Fav, FavAdmin)