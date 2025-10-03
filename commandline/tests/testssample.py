from io import StringIO
import sys

from django.test import TestCase
from django.core import management


from career.models import Company


class AddTests(TestCase):

    def test_success_add_sample(self):
        err = StringIO()
        sys.stdin = StringIO('Snap\nSnap@email.com\n09122201202\nOnline Taxi\n')
        management.call_command('addCompany', stderr=err)
        quera = Company.objects.get(name='Snap')
        self.assertEqual(quera.email, 'Snap@email.com')
        self.assertEqual(quera.phone, '09122201202')
        self.assertEqual(quera.description, 'Online Taxi')
        self.assertEqual(err.getvalue(), '')


class EditTest(TestCase):
    def setUp(self):
        Company.objects.create(name='Quera', email="quera@email.com", phone="09122201202", description="a place for programmers")

    def test_success_edit(self):
        try:
            management.call_command('editCompany', 'Quera', name='quera', email="Quera@email.com", phone="+989112201202", description="Programming Contest")
        except:
            self.fail("unexpected CommandError!")
        quera = Company.objects.get(name="quera")
        self.assertEqual(quera.email, "Quera@email.com")
        self.assertEqual(quera.phone, "+989112201202")
        self.assertEqual(quera.description, "Programming Contest")


class RemoveTest(TestCase):
    def setUp(self):
        self.quera = Company.objects.create(name='Quera', email="quera@email.com", phone="09122201202", description="a place for programmers")
        self.yektanet = Company.objects.create(name='yektanet', email="Yektanet@email.com", phone="09122201203")
        self.snap = Company.objects.create(name='snap', email="snap@email.com", phone="09122201204")

    def test_remove_all(self):
        try:
            err = StringIO()
            management.call_command('rmCompany', stderr=err, all=True)
        except:
            self.fail("unexpected CommandError!")
        self.assertEqual(Company.objects.all().count(), 0)
        self.assertEqual(err.getvalue(), '')
