from functools import wraps
from django.http import Http404, HttpResponseForbidden, HttpResponse
from projects.models import ProjectMembership


class projects_panel(object):
    def __init__(self, permissions=None):
        self.permissions = permissions

    def __call__(self, view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            user = request.user

            # Fetch all memberships for the user
            memberships = ProjectMembership.objects.filter(user=user)

            # If no memberships found, return a 404 response
            if not memberships.exists():
                return HttpResponse("No projects found", status=404)

            request.memberships = memberships

            # Find current membership; if none, pick the one with smallest ID
            current_membership = memberships.filter(is_current=True).first()
            if not current_membership:
                current_membership = memberships.order_by("id").first()
                current_membership.is_current = True
                current_membership.save()

            request.current_membership = current_membership
            request.project = current_membership.project

            # Check permissions if specified
            if self.permissions:
                for perm in self.permissions:
                    if not current_membership.has_permission(perm):
                        return HttpResponseForbidden(
                            "You do not have permission to perform this action."
                        )

            return view_func(request, *args, **kwargs)

        return _wrapper_view
