from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from model_utils.models import TimeStampedModel

import uuid

class Genre(TimeStampedModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'genre'

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    first_name = models.CharField(_('first name'), max_length=255)
    second_name = models.CharField(_('second name'), max_length=255)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'person'

    def __str__(self):
        return f'{self.first_name} {self.second_name}'


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    SERIES = 'series', _('series')


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    certificate = models.TextField(_('certificate'), blank=True, null=True)
    file_path = models.FileField(_('file path'), upload_to='film_works/', blank=True, null=True)
    rating = models.FloatField(_('rating'),
                               validators=[MinValueValidator(0)], blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')
    type = models.CharField(_('type'), choices=FilmworkType.choices, max_length=20)

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = 'film_work'

    def __str__(self):
        return self.title


class PersonRole(models.TextChoices):
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')
    ACTOR = 'actor', _('actor')


class PersonFilmwork(TimeStampedModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=PersonRole.choices, blank=True)

    class Meta:
        db_table = 'person_film_work'
        indexes = [
            models.Index(fields=['film_work', 'person', 'role'], name='film_work_person_role_idx'),
        ]
        unique_together = [['person', 'film_work', 'role']]
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class GenreFilmwork(TimeStampedModel):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)

    class Meta:
        db_table = 'genre_film_work'
        indexes = [
            models.Index(fields=['genre', 'film_work'], name='genre_film_work_idx'),
        ]
        unique_together = [['genre', 'film_work']]
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
