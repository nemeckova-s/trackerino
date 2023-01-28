from rest_framework import serializers

from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reporter = serializers.StringRelatedField()
    assignee = serializers.StringRelatedField()

    class Meta:
        model = Issue
        fields = (
            'id',
            'title',
            'description',
            'category',
            'current_state',
            'reporter',
            'assignee',
        )
