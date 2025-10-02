from django.urls import path

from projects.activation_view import active_project
from projects.views import *

urlpatterns = [
    path('', index, name='index'),
    path('remove/', remove_project, name='remove_project'),
    path('add-member/', add_team_member, name='add_member_project'),
    path('merge-a-request/', merge_project, name='merge_a_request'),

    path('<int:project_id>/active/', active_project, name='active_project'),
]
