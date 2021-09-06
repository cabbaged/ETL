import django
import factory
import os
import random
import sys
import uuid

from django.db.utils import IntegrityError

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth.models import User
from movies.models import Genre, Filmwork, Person


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    first_name = factory.Faker('first_name')
    second_name = factory.Faker('last_name')


class FilmworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filmwork

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if extracted:
            self.genre.set(extracted)

    @factory.post_generation
    def persons(self, create, extracted, **kwargs):
        if extracted:
            self.persons.set(extracted)

    title = factory.Sequence(lambda n: "filmwork title %03d" % n)
    type = factory.Iterator(('movie', 'series'))
    creation_date = factory.Faker('date')


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: "genre name %03d" % n)
    description = factory.Sequence(lambda n: "genre description %03d" % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%03d' % n)
    email = factory.LazyAttribute(lambda u: f'{u.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password',
                                                uuid.uuid4().hex)  # factory.Faker(lambda _: uuid.uuid4().hex)


if __name__ == '__main__':
    batches = 10001
    for i in range(1, batches + 1):
        print(f'generating batch {i} out of {batches}')
        try:
            UserFactory()
            ps = PersonFactory.create_batch(50)
            gs = GenreFactory.create_batch(10)
            FilmworkFactory.create_batch(100,
                                         genre=random.sample(gs, k=random.randint(0, 3)),
                                         persons=random.sample(ps, k=random.randint(0, 5))
                                         )
        except IntegrityError as e:
            print('skipping')
            print(e)
    print("finished")
