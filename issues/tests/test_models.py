import datetime

from django.test import TestCase

from django.contrib.auth.models import User

from issues.models import Issue, Category, IssueStateChange
from issues.time_deltas import TimeDeltas


class TestIssue(TestCase):
    """
    Test the Issue model and its manager.
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user('userA', '', 'password')
        self.category = Category.objects.create(name='Category A')

    def test_default_state_created_on_create(self):
        """
        Check that when calling `Issue.objects.create`, a default state change is created, too.
        """
        issue = Issue.objects.create(
            title='Testing issue A',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        self.assertIsNotNone(issue.last_state_change)
        self.assertEqual(issue.last_state_change.new_state, IssueStateChange.DEFAULT_STATE)

    def test_default_state_created_on_save(self):
        """
        Check that when calling the `save` method on an `Issue` instance without a state,
        a default state change is created.
        """
        issue = Issue(
            title='Testing issue B',
            reporter=self.user,
            assignee=self.user,
            description='abcde',
            category=self.category,
        )
        issue.save()
        self.assertIsNotNone(issue.last_state_change)
        self.assertEqual(issue.last_state_change.new_state, IssueStateChange.DEFAULT_STATE)

    def test_save_set_new_state(self):
        """
        Check that calling the `save` method on an `Issue` instance with `_set_new_state`
        set to a new `IssueStateChange.State`, the current state of the issue is updated.
        """
        issue = Issue.objects.create(
            title='Testing issue C',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        issue._set_new_state = IssueStateChange.State.DONE
        issue.save()
        self.assertEqual(issue.last_state_change.new_state, IssueStateChange.State.DONE)

    def test_get_resolving_times_empty(self):
        """
        Test the `Issue.objects.get_resolving_times` method
        when there are no DONE issues in the database.
        """
        # Prepare testing data.
        Issue.objects.create(
            title='Testing issue 1',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        issue2 = Issue.objects.create(
            title='Testing issue 2',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        issue2.update_state(IssueStateChange.State.IN_PROGRESS)
        issue3 = Issue.objects.create(
            title='Testing issue 3',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        issue3.update_state(IssueStateChange.State.CANCELED)

        # Call the tested method.
        resolving_times = Issue.objects.get_resolving_times()
        self.assertIsInstance(resolving_times, TimeDeltas)
        self.assertEqual(resolving_times.times, [])

    def test_get_resolving_times_not_empty(self):
        """
        Test the `Issue.objects.get_resolving_times` method
        when there are some DONE issues in the database.
        """
        # Prepare testing data.
        issue1 = Issue.objects.create(
            title='Testing issue 1',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        created_at = issue1.last_state_change.occurred_at
        # Change the state of the issue a few times - only
        # the first and the last change should matter.
        issue1.update_state(IssueStateChange.State.IN_PROGRESS)
        issue1.update_state(IssueStateChange.State.TO_DO)
        issue1.update_state(IssueStateChange.State.IN_PROGRESS)
        issue1.update_state(IssueStateChange.State.DONE)
        issue1.update_state(IssueStateChange.State.IN_PROGRESS)
        issue1.update_state(
            IssueStateChange.State.DONE,
            occurred_at=created_at + datetime.timedelta(minutes=30),
        )

        issue2 = Issue.objects.create(
            title='Testing issue 2',
            reporter=self.user,
            assignee=self.user,
            description='',
            category=self.category,
        )
        created_at = issue2.last_state_change.occurred_at
        issue2.update_state(
            IssueStateChange.State.DONE, occurred_at=created_at + datetime.timedelta(hours=6),
        )

        # Call the tested method.
        resolving_times = Issue.objects.get_resolving_times()
        self.assertIsInstance(resolving_times, TimeDeltas)
        self.assertEqual(
            set(resolving_times.times),
            {datetime.timedelta(minutes=30), datetime.timedelta(hours=6)},
        )
