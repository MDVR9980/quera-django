from django.contrib.auth.models import User
from django.db import models, transaction


class Project(models.Model):
    name = models.CharField(max_length=100)


class ProjectMembership(models.Model):
    ROLE_GUEST = "RG"
    ROLE_REPORTER = "RR"
    ROLE_DEVELOPER = "RD"
    ROLE_MASTER = "RM"
    ROLE_OWNER = "RO"

    ROLE_CHOICES = (
        (ROLE_GUEST, "Guest"),
        (ROLE_REPORTER, "Reporter"),
        (ROLE_DEVELOPER, "Developer"),
        (ROLE_MASTER, "Master"),
        (ROLE_OWNER, "Owner"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=4, choices=ROLE_CHOICES, default=ROLE_GUEST, verbose_name="Role"
    )
    is_current = models.BooleanField(default=False)

    def has_permission(self, action):
        """
        Check if the user has permission to perform a specific action based on their role.

        Args:
            action (str): Action in snake_case format.

        Returns:
            bool: True if allowed, False otherwise.
        """
        # Map actions to allowed roles
        permissions_map = {
            "create_new_issue": ["RG", "RR", "RD", "RM", "RO"],
            "leave_comments": ["RG", "RR", "RD", "RM", "RO"],
            "pull_project_code": ["RR", "RD", "RM", "RO"],
            "assign_issues_and_merge_requests": ["RR", "RD", "RM", "RO"],
            "see_a_list_of_merge_requests": ["RR", "RD", "RM", "RO"],
            "manage_merge_requests": ["RD", "RM", "RO"],
            "create_new_branches": ["RD", "RM", "RO"],
            "add_new_team_members": ["RM", "RO"],
            "push_to_protected_branches": ["RM", "RO"],
            "switch_visibility_level": ["RO"],
            "remove_project": ["RO"],
            "force_push_to_protected_branches": [],
        }

        allowed_roles = permissions_map.get(action, [])
        # Return True if the user's role is in allowed roles
        return self.role in allowed_roles

    class Meta:
        unique_together = ("user", "project")
