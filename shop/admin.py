from django.contrib import admin
from django.db.models import Avg

from .models import Boardgame, Category, Publisher, Review


class BoardgameAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'publisher')
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('boardgame', 'rating', 'user')


admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Review, ReviewAdmin)
