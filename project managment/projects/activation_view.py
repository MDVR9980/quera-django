from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.db import transaction

from projects.models import ProjectMembership, Project


def active_project(request, project_id):
    """
    Activate a project as the current project for the logged-in user.

    Steps:
    1. Ensure the project exists.
    2. Ensure the user has a membership in this project.
    3. Update all other memberships of the user to is_current=False.
    4. Set this membership as is_current=True.
    5. Redirect to the index page.
    """
    user = request.user

    # Fetch the project or return 404 if it doesn't exist
    project = get_object_or_404(Project, pk=project_id)

    # Fetch membership for the user in this project
    try:
        membership = ProjectMembership.objects.get(user=user, project=project)
    except ProjectMembership.DoesNotExist:
        raise Http404("Membership not found for this project")

    # Use transaction to avoid race conditions
    with transaction.atomic():
        # Set all other memberships to is_current=False
        ProjectMembership.objects.filter(user=user, is_current=True).update(
            is_current=False
        )
        # Activate this membership
        membership.is_current = True
        membership.save()

    # Redirect to the index page
    return redirect("index")
