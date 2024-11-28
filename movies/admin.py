# movies/admin.py

from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    # Display fields in the list
    list_display = ('name', 'created', 'modified')
    # Поиск по полям
    # Search by fields
    search_fields = ('name',)
    # Фильтрация в списке
    # Filtering in the list
    list_filter = ('created', 'modified')
    empty_value_display = '--пусто--'
    # inlines = (GenreFilmworkInline,)

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'rating', 'type', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('creation_date', 'rating', 'type', 'created', 'modified')
    empty_value_display = '--пусто--'
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name',)
    list_filter = ('created', 'modified')
    empty_value_display = '--пусто--'
    # inlines = (PersonFilmworkInline,)
