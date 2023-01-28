from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from issues.models import Issue, Category


class TestIssueDetailView(TestCase):
    """
    Test the Issue detail view.
    """

    def _get_url(self, issue_id: int) -> str:
        return reverse('admin:issues_issue_change', args=(issue_id,))

    def setUp(self):
        # Prepare the client and some users.
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin', email='admin@trackerino.cz'
        )
        self.staff_user = User.objects.create_user(
            username='staff', password='staff', email='staff@trackerino.cz', is_staff=True
        )
        self.common_user = User.objects.create_user(
            username='common', password='common', email='common@trackerino.cz'
        )

        # Create testing data.
        self.category = Category.objects.create(name='Testing category 1')
        self.issue = Issue.objects.create(
            title='Testing issue 1',
            description='Desription of testing issue 1',
            category=self.category,
            reporter=self.superuser,
            assignee=self.staff_user,
        )

    def _change_view_success(self):
        response = self.client.get(self._get_url(self.issue.pk))
        self.assertEqual(response.status_code, 200)

    def test_change_view__superuser(self):
        """
        Test that a superuser can load the issue change form.
        """
        self.client.force_login(self.superuser)
        self._change_view_success()

    def test_change_view__staff_user(self):
        """
        Test that a staff user can load the issue change form.
        """
        self.client.force_login(self.staff_user)
        self._change_view_success()

    def test_change_view_for__common_user(self):
        """
        Test that a non-staff user cannot load the issue change form.
        """
        self.client.force_login(self.common_user)
        response = self.client.get(self._get_url(self.issue.pk))
        self.assertEqual(response.status_code, 302)

    def test_change_view_for__invalid_issue_id(self):
        """
        Test that issue form with invalid issue ID.
        """
        self.client.force_login(self.superuser)
        response = self.client.get(self._get_url(123))
        self.assertEqual(response.status_code, 302)
