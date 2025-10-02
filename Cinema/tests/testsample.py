from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse


class TestMovieFixture(TestCase):
    exception_fixtures = False
    my_fixtures = ['movies', ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for db_name in cls._databases_names(include_mirrors=False):
            try:
                call_command('loaddata', *cls.my_fixtures, **{'verbosity': 0, 'database': db_name})
            except Exception:
                cls.exception_fixtures = True

    def test_load_movie_fixture(self):
        self.assertFalse(self.exception_fixtures)


class TestSeatFixture(TestCase):
    exception_fixtures = False
    my_fixtures = ['seats', ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for db_name in cls._databases_names(include_mirrors=False):
            try:
                call_command('loaddata', *cls.my_fixtures, **{'verbosity': 0, 'database': db_name})
            except Exception:
                cls.exception_fixtures = True

    def test_load_seat_fixture(self):
        self.assertFalse(self.exception_fixtures)


class TestTicket(TestCase):
    fixtures = ['movies', 'seats']

    def setUp(self):
        self.user = User.objects.create_user("meysam", "meysam@kazemi.ir", "123456")

    def test_movie_list(self):
        c = Client()
        res = c.get(reverse('list_movies'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Children of heaven', html=True, count=1)
        self.assertContains(res, 'About Elly', html=True, count=1)
        self.assertContains(res, 'A separation', html=True, count=1)
        self.assertContains(res, 'The salesman', html=True, count=1)
        self.assertContains(res, 'The Elephant king', html=True, count=1)
        self.assertContains(res, '<li>', count=5)
