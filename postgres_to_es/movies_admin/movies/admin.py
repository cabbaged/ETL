from django.contrib import admin
from .models import Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')

    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    )

    inlines = [
        PersonFilmworkInline,
        GenreFilmworkInline
    ]

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'birth_date', 'created', 'modified')
    list_filter = ('second_name',)
    search_fields = ('second_name', 'id')
    fields = ('first_name', 'second_name', 'birth_date',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('name',)
    search_fields = ('name', 'id')
    fields = ('name', 'description')
