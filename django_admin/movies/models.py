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

    filmworks = models.ManyToManyField(
        'Filmwork',
        through='GenreFilmwork',
        verbose_name=_('film'),
    )

    def __str__(self):
        return self.name

    class Meta:
        # Если таблицы находятся в нестандартной схеме, это нужно указать в классе модели
        # If the tables are in a non-standard schema, this must be specified in the model class
        db_table = 'content"."genre'
        # Названия модели в интерфейсе администратора Django.
        # Model names in the Django admin interface.
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.CharField(_('full_name'), max_length=255)
    gender = models.TextField(
        _('gender'),
        choices=Gender.choices,
        null=True,
        blank=True,
    ) 

    film_works = models.ManyToManyField(
        'Filmwork',
        through='PersonFilmwork',
        verbose_name=_('film'),
    )

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'content"."person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmTypes(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv show', _('tv show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0),
        ],
    )
    type = models.CharField(
        _('type'),
        max_length=7,
        choices=FilmTypes.choices,
        default=FilmTypes.MOVIE,
    )
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы. 
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    # The upload_to parameter specifies in which subfolder the uploaded files will be stored.
    # The base folder is specified in the settings file as MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)

    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmWork',
        verbose_name=_('genres'),
    )
    persons = models.ManyToManyField(
        Person,
        through='PersonFilmwork',
        verbose_name=_('persons'),
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('film')
        verbose_name_plural = _('films')
        ordering = ['-creation_date']
        indexes = [
            models.Index(
                fields=['creation_date', 'rating'],
                name='film_work_creation_rating_idx',
            ),
        ]

class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        verbose_name=_('film'),
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_('genre'),
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.genre.name

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('genre of filmwork')
        verbose_name_plural = _('genres of filmworks')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='film_work_genre_idx',
            ),
        ]
 

class PersonFilmwork(UUIDMixin):
    class Roles(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        verbose_name=_('film'),
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )
    role = models.CharField(
        _('role'),
        max_length=50,
        choices=Roles.choices,
        default=Roles.ACTOR,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('person of film')
        verbose_name_plural = _('persons of film')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_role_idx',
            ),
        ]



