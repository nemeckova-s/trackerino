from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Issue(models.Model):

    reporter = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='reported_issues'
    )
    assignee = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='assigned_issues'
    )
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    last_state_change = models.ForeignKey(
        'IssueStateChange',
        on_delete=models.RESTRICT,
        related_name='current_state_issue',
        null=True,
        blank=True,
        editable=False,
    )
    # TODO: Create a foreign key on (id, last_state_change_id)
    #  referencing IssueStateChange(issue_id, id).

    def __str__(self):
        return self.description

    def current_state(self):
        return getattr(self.last_state_change, 'new_state', IssueStateChange.State.TO_DO).label


class IssueStateChange(models.Model):
    class State(models.TextChoices):
        TO_DO = 'TO_DO', gettext_lazy('TO DO')
        IN_PROGRESS = 'IN_PROGRESS', gettext_lazy('IN PROGRESS')
        DONE = 'DONE', gettext_lazy('DONE')
        CANCELED = 'CANCELED', gettext_lazy('CANCELED')

    issue = models.ForeignKey(Issue, on_delete=models.RESTRICT)
    new_state = models.CharField(max_length=20, choices=State.choices, default=State.TO_DO)
    occurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.new_state
