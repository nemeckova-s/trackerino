from django.contrib import admin

from issues.forms import IssueForm
from issues.models import Category, Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'assignee',
        'reporter',
        'current_state',
    )
    ordering = ('last_state_change__new_state', 'last_state_change__occurred_at')
    list_filter = ('category',)
    search_fields = ('description__startswith',)
    form = IssueForm

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['resolving_times'] = Issue.objects.get_resolving_times()
        return super(IssueAdmin, self).changelist_view(request, extra_context=extra_context)


admin.site.register(Category)
