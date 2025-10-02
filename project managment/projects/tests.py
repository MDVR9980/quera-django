from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from projects.models import Project, ProjectMembership


class SampleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'user@projects.com', 'SecretPassword')
        self.project1 = Project.objects.create(name='first sample project')
        self.project2 = Project.objects.create(name='second sample project')

    def test_sample_1(self):
        c = Client()
        c.force_login(user=self.user)
        res = c.get(reverse('index'))
        self.assertEquals(res.status_code, 404)
        self.assertTrue('no projects found' in res.content.decode().lower())

        membership1 = ProjectMembership.objects.create(user=self.user, project=self.project1, role='RD')
        self.assertFalse(membership1.is_current)

        res = c.get(reverse('index'))
        self.assertEquals(res.status_code, 200)
        self.assertFalse('no projects found' in res.content.decode().lower())
        membership1.refresh_from_db()
        self.assertTrue(membership1.is_current)

        membership2 = ProjectMembership.objects.create(user=self.user, project=self.project2, role='RO')
        self.assertFalse(membership2.is_current)

        res = c.get(reverse('active_project', args=[self.project2.id]), follow=True)
        self.assertEquals(res.status_code, 200)
        self.assertFalse('no projects found' in res.content.decode().lower())

        membership1.refresh_from_db()
        membership2.refresh_from_db()

        self.assertFalse(membership1.is_current)
        self.assertTrue(membership2.is_current)

    def test_sample_2(self):
        membership = ProjectMembership.objects.create(user=self.user, project=self.project2, role='RD')
        self.assertTrue(membership.has_permission('pull_project_code'))
        self.assertTrue(membership.has_permission('create_new_branches'))
        self.assertFalse(membership.has_permission('add_new_team_members'))
        self.assertFalse(membership.has_permission('remove_project'))

        membership.role = 'RO'
        membership.save()

        self.assertTrue(membership.has_permission('remove_project'))
        self.assertFalse(membership.has_permission('force_push_to_protected_branches'))

    def test_sample_3(self):
        c = Client()
        c.force_login(user=self.user)
        membership1 = ProjectMembership.objects.create(user=self.user, project=self.project1, role='RD')
        res = c.get(reverse('index'))
        self.assertEquals(res.status_code, 200)
        membership1.refresh_from_db()
        self.assertTrue(membership1.is_current)

        res = c.get(reverse('remove_project'))
        self.assertTrue(res.status_code, 403)
