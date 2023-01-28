from __future__ import annotations

import datetime

from django.contrib.auth.models import User
from django.db import models, transaction, connection
from django.utils.translation import gettext_lazy

from issues.resolving_times import TimeDeltas


class Category(models.Model):
    """
    Categories of issues.
    """

    CATEGORY_MAX_LENGTH = 50

    name = models.CharField(max_length=CATEGORY_MAX_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class IssueManager(models.Manager):
    def get_resolving_times(self) -> TimeDeltas:
        """
        For each issue in state "DONE", calculate the time it took for it do be marked as "DONE"
        (from the moment the issue was created).
        """
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select round((
                    julianday(max(done.occurred_at))
                    - julianday(min(created.occurred_at))
                ) * 86400)
                from issues_issue i
                join issues_issuestatechange done on done.id = i.last_state_change_id
                join issues_issuestatechange created on created.issue_id = i.id
                where done.new_state = %s
                group by i.id
                """,
                (IssueStateChange.State.DONE.value,),
            )
            results = cursor.fetchall()
        return TimeDeltas([datetime.timedelta(seconds=r[0]) for r in results])


class Issue(models.Model):

    TITLE_MAX_LENGTH = 80

    _set_new_state = None

    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    reporter = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='reported_issues'
    )
    assignee = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='assigned_issues'
    )
    last_state_change = models.OneToOneField(
        'IssueStateChange',
        on_delete=models.RESTRICT,
        related_name='current_state_issue',
        null=True,
        blank=True,
        editable=False,
    )
    # TODO: Create a foreign key on (id, last_state_change_id)
    #  referencing IssueStateChange(issue_id, id).

    objects = IssueManager()

    @property
    def current_state(self) -> str:
        """
        Get human-freindly label of the current state of this issue.
        """
        return self.last_state_change.new_state_choice.label

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        with transaction.atomic():
            super(Issue, self).save(*args, **kwargs)
            # If the issue does not have a state yet, or if its current change should be changed
            # (see issues.forms.IssueForm.save method), create/update it.
            if self.last_state_change is None or self._set_new_state is not None:
                new_state = self._set_new_state or IssueStateChange.DEFAULT_STATE
                self._set_new_state = None
                self.update_state(new_state)

    def update_state(self, new_state: IssueStateChange.State):
        self.last_state_change = IssueStateChange.objects.create(
            issue=self, new_state=new_state,
        )
        self.save(update_fields=('last_state_change_id',))


class IssueStateChange(models.Model):
    """
    Historized changes of issues' states.
    """

    class State(models.TextChoices):
        TO_DO = 'TO_DO', gettext_lazy('TO DO')
        IN_PROGRESS = 'IN_PROGRESS', gettext_lazy('IN PROGRESS')
        DONE = 'DONE', gettext_lazy('DONE')
        CANCELED = 'CANCELED', gettext_lazy('CANCELED')

    STATE_MAX_LENGTH = 20
    DEFAULT_STATE = State.TO_DO

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    new_state = models.CharField(
        max_length=STATE_MAX_LENGTH, choices=State.choices, default=DEFAULT_STATE
    )
    occurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.new_state

    @property
    def new_state_choice(self) -> IssueStateChange.State:
        return IssueStateChange.State(self.new_state)
