from django.contrib import admin
from .models import Environment, Node, NodeTag, SSHUser


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'primary_address', 'secondary_address', 'env']
    list_filter = ['env', 'tags']
    filter_horizontal = ['tags']
    search_fields = ['name', 'desc', 'primary_address', 'secondary_address']


@admin.register(NodeTag)
class NodeTagAdmin(admin.ModelAdmin):
    pass


@admin.register(SSHUser)
class SSHUserAdmin(admin.ModelAdmin):
    pass
