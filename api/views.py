from rest_framework import viewsets
from rest_framework import permissions

from issues.models import Issue
from issues.serializers import IssueSerializer


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows issues to be viewed.
    """

    queryset = Issue.objects.all().order_by('title')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAdminUser]
