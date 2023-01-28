from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from issues.models import Issue, Category, IssueStateChange


class TestIssuesAPI(TestCase):
    LIST_ISSUES_URL = '/api/issues/'
    ISSUE_DETAIL_URL = '/api/issues/%s/'

    def setUp(self) -> None:
        self.client = APIClient()
        self.superuser_raw_password = 'password1234'
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@trackerino.cz', self.superuser_raw_password
        )
        self.staff_user_raw_password = 'staff'
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@trackerino.cz',
            password=self.staff_user_raw_password,
            is_staff=True,
        )
        self.common_user = User.objects.create_user(
            username='common', email='common@trackerino.cz', password='common'
        )

    def test_issues_list_superuser_session(self):
        """
        Check that the API for listing issues can be called by a superuser, using session login.
        """
        self.client.login(
            username=self.superuser.username, password=self.superuser_raw_password
        )
        response = self.client.get(self.LIST_ISSUES_URL)
        self.assertEqual(response.status_code, 200)
        assert response.json() == []

    def test_issues_list_staff_token(self):
        """
        Check that the API for listing issues can be called by a staff user, using token login.
        """
        response = self.client.get(
            self.LIST_ISSUES_URL,
            HTTP_AUTHORIZATION=f'Token {Token.objects.get(user=self.staff_user).key}',
        )
        self.assertEqual(response.status_code, 200)
        assert response.json() == []

    def test_issues_list_common_token(self):
        """
        Check that the API for listing issues cannot be called by a non-staff user.
        """
        response = self.client.get(
            self.LIST_ISSUES_URL,
            HTTP_AUTHORIZATION=f'Token {Token.objects.get(user=self.common_user).key}',
        )
        self.assertEqual(response.status_code, 403)

    def test_issues_list_not_empty(self):
        """
        Check that the API for listing issues returns all issues in the expected format.
        """
        category1 = Category.objects.create(name='Cat1')
        category2 = Category.objects.create(name='Cat2')
        issue1 = Issue.objects.create(
            title='Testing issue 1',
            description='',
            category=category1,
            reporter=self.superuser,
            assignee=self.staff_user,
        )
        issue2 = Issue.objects.create(
            title='Testing issue 2',
            description='Desciption ABC',
            category=category2,
            reporter=self.superuser,
            assignee=self.superuser,
        )
        issue2.update_state(IssueStateChange.State.DONE)
        response = self.client.get(
            self.LIST_ISSUES_URL,
            HTTP_AUTHORIZATION=f'Token {Token.objects.get(user=self.superuser).key}',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id': issue1.id,
                    'title': issue1.title,
                    'description': issue1.description,
                    'category': issue1.category.name,
                    'current_state': issue1.current_state,
                    'reporter': issue1.reporter.username,
                    'assignee': issue1.assignee.username,
                },
                {
                    'id': issue2.id,
                    'title': issue2.title,
                    'description': issue2.description,
                    'category': issue2.category.name,
                    'current_state': issue2.current_state,
                    'reporter': issue2.reporter.username,
                    'assignee': issue2.assignee.username,
                },
            ],
        )

    def test_issue_detail_superuser(self):
        """
        Check that the API for fetching an issue can be called by a superuser using a token login
        and returns the issue in the expected format.
        """
        category1 = Category.objects.create(name='Cat1')
        issue = Issue.objects.create(
            title='Testing issue 1',
            description='',
            category=category1,
            reporter=self.superuser,
            assignee=self.staff_user,
        )
        response = self.client.get(
            self.ISSUE_DETAIL_URL % issue.id,
            HTTP_AUTHORIZATION=f'Token {Token.objects.get(user=self.superuser).key}',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id': issue.id,
                'title': issue.title,
                'description': issue.description,
                'category': issue.category.name,
                'current_state': issue.current_state,
                'reporter': issue.reporter.username,
                'assignee': issue.assignee.username,
            },
        )

    def test_issue_detail_staff_session(self):
        """
        Check that the API for fetching an issue can be called by a staff user using a session login
        and returns the issue in the expected format.
        """
        self.client.login(
            username=self.staff_user.username, password=self.staff_user_raw_password
        )
        category = Category.objects.create(name='Cat1')
        issue = Issue.objects.create(
            title='Testing issue X',
            description='',
            category=category,
            reporter=self.superuser,
            assignee=self.superuser,
        )
        issue.update_state(IssueStateChange.State.IN_PROGRESS)
        response = self.client.get(self.ISSUE_DETAIL_URL % issue.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id': issue.id,
                'title': issue.title,
                'description': issue.description,
                'category': issue.category.name,
                'current_state': issue.current_state,
                'reporter': issue.reporter.username,
                'assignee': issue.assignee.username,
            },
        )

    def test_issue_detail_invalid_issue_id(self):
        """
        Test the issue details API with an invalid issue ID.
        """
        self.client.login(
            username=self.staff_user.username, password=self.staff_user_raw_password
        )
        # Not a number.
        response = self.client.get(self.ISSUE_DETAIL_URL % 'abc')
        self.assertEqual(response.status_code, 404)
        # An issue with this ID does not exist.
        response = self.client.get(self.ISSUE_DETAIL_URL % 666)
        self.assertEqual(response.status_code, 404)
