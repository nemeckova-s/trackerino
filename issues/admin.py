from django.contrib import admin

from issues.models import Category, Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'category',
        'assignee',
        'reporter',
        'current_state',
    )


admin.site.register(Category)
