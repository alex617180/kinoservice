# movies/admin.py

from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)

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
    empty_value_display = _('--empty--')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name',)
    list_filter = ('created', 'modified')
    empty_value_display = _('--empty--')

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres', 'get_persons')
    search_fields = ('title', 'description', 'id')
    list_filter = ('type', 'genres')
    empty_value_display = _('--empty--')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    def get_queryset(self, request):
        # Оптимизируем запросы для жанров и персон
        # Optimize queries for genres and persons
        queryset = super().get_queryset(request).prefetch_related('genres', 'person_film_work__person')
        return queryset

    def get_genres(self, obj):
        # Возвращаем строку с жанрами
        # Return a string with genres
        return ', '.join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = _('genres')

    def get_persons(self, obj):
        # Возвращаем строку с персональными данными (роль и полное имя)
        # Return a string with personal data (role and full_name)
        persons = obj.person_film_work.all()
        return ', '.join([f"{person.person.full_name} ({person.role})" for person in persons])
    get_persons.short_description = _('persons')

