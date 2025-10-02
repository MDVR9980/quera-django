from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from projects.decorators import projects_panel


@login_required
@projects_panel()
def index(request):
    return render(request, 'projects/project_home.html', context={
        'project': request.project,
        'current_membership': request.current_membership,
        'memberships': request.memberships,
    })


@login_required
@projects_panel(permissions=['add_new_team_members'])
def add_team_member(request):
    return HttpResponse('member added - OK')


@login_required
@projects_panel(permissions=['remove_project'])
def remove_project(request):
    request.project.delete()
    return redirect('index')


@login_required
@projects_panel(permissions=['see_a_list_of_merge_requests', 'manage_merge_requests'])
def merge_project(request):
    return HttpResponse('merge project - OK')
