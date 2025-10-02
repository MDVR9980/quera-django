from django.test import TestCase, Client
from django.urls import reverse

from account.models import *
from account.views import *
from account.forms import *


class TestAll(TestCase):

    def test_login_success_redirect(self):
        Account.objects.create(username="test1", password="test1pass")
        account = Account.objects.get(username="test1")
        account.set_password("test1pass")
        account.save()
        bar_path = reverse('home')
        response = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'test1pass'})
        self.assertEqual(response['Location'], bar_path)

    def test_login_failed_redirect(self):
        Account.objects.create(username="test1", password="test1pass")
        account = Account.objects.get(username="test1")
        account.set_password("test1pass")
        account.save()
        bar_path = reverse('login')
        response = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'pass'})
        self.assertEqual(response['Location'], bar_path)

    def test_signup(self):
        response = self.client.post(reverse('signup'), data={'username': 'sajjad', 'email': 'Sajjad123@gmail.com',
                                                             'password1': 'Farahan123', 'password2': 'Farahan123'})
        try:
            account = Account.objects.get(username="sajjad")
        except Account.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(1, 1)

    def test_join_or_create_team1(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        team = Team.objects.create(name='dishdish', jitsi_url_path='dishdish')
        account.team = team
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.get(reverse('team'))
        self.assertEqual(response.url, '/home/')

    def test_join_or_create_team2(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        self.client.login(username='sajjad', password='123')
        self.client.post(reverse('team'), data={'name': 'filan'})
        try:
            team = Team.objects.get(name='filan')
        except Team.DoesNotExist:
            self.assertEqual(1, 2)
        if team.jitsi_url_path != 'http://meet.jit.si/filan':
            self.assertEqual(2, 3)
        self.assertEqual(1, 1)

    def test_join_or_create_team_redirect(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.post(reverse('team'), data={'name': 'filan'})
        self.assertEqual(response.url, '/home/')


    def test_exit_team(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        team = Team.objects.create(name='dishdish', jitsi_url_path='dishdish')
        account.team = team
        account.save()
        self.client.login(username='sajjad', password='123')
        self.client.get(reverse('exit'))
        self.assertEqual(Account.objects.get(username="sajjad").team, None)

    def test_home_1(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        team = Team.objects.create(name='dishdish', jitsi_url_path='dishdish')
        account.team = team
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'dishdish')

    def test_home_2(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'None')


    def test_join_or_create_team_redirect(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.post(reverse('team'), data={'name': 'filan'})
        self.assertEqual(response.url, '/home/')


    def test_exit_team(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        team = Team.objects.create(name='dishdish', jitsi_url_path='dishdish')
        account.team = team
        account.save()
        self.client.login(username='sajjad', password='123')
        self.client.get(reverse('exit'))
        self.assertEqual(Account.objects.get(username="sajjad").team, None)

    def test_home_1(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        team = Team.objects.create(name='dishdish', jitsi_url_path='dishdish')
        account.team = team
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'dishdish')

    def test_home_2(self):
        account = Account.objects.create(username='sajjad')
        account.set_password('123')
        account.save()
        self.client.login(username='sajjad', password='123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'None')
