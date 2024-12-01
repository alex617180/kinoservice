# movies/models.py
# Определение моделей приложения.

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    # auto_now_add will automatically set the date when the record was created
    created = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    # auto_now will change every time the record is updated
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы в базе данных.
        # This parameter tells Django that this class is not a representation of a table in the database.
        abstract = True


class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    # A typical model in Django uses a number as an id. In such situations, the field is not described in the model.
    # You will have to explicitly declare the primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        

class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    # blank=True делает поле необязательным для заполнения.
    # blank=True makes the field optional.
    description = models.TextField(_('description'), blank=True, null=True)

    filmworks = models.ManyToManyField('Filmwork', through='GenreFilmwork')

    def __str__(self):
        return self.name

    class Meta:
        # Если таблицы находятся в нестандартной схеме, это нужно указать в классе модели
        # If the tables are in a non-standard schema, this must be specified in the model class
        db_table = "content\".\"genre"
        # Названия модели в интерфейсе администратора Django.
        # Model names in the Django admin interface.
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=50, choices=Type.choices, default=Type.MOVIE)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы. 
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    # The upload_to parameter specifies in which subfolder the uploaded files will be stored.
    # The base folder is specified in the settings file as MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.CharField(_('full_name'), max_length=255)
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True) 

    film_works = models.ManyToManyField(Filmwork, through='PersonFilmwork')

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of filmwork')
        verbose_name_plural = _('Genres of filmworks') 

class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person of filmwork')
        verbose_name_plural = _('Persons of filmworks')



