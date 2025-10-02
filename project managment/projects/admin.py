from django.contrib import admin

from projects.models import *


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'role', 'is_current')

    def project_name(self, mem):
        return mem.project.name
