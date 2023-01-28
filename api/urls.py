from django.urls import path, include
from rest_framework import routers

from api import views

app_name = 'issues'

router = routers.DefaultRouter()
router.register(r'issues', views.IssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
