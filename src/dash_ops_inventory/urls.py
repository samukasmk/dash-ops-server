from django.conf.urls import url, include
from django.contrib import admin
from .views import rundeck_nodes_by_env
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # /api/inventory/rundeck_nodes/1
    url(r'rundeck_nodes/(?P<env_id>[0-9]+)/$',
        rundeck_nodes_by_env,
        name='rundeck_nodes_by_env_id'),

    # /api/inventory/rundeck_nodes/my_environment_name
    url(r'rundeck_nodes/(?P<env_name>[a-zA-Z0-9\.\-\_]*)/$',
        rundeck_nodes_by_env,
        name='rundeck_nodes_by_env_name'),

    ### ACCEPTABLED GET PARAMS
    # .../?domain_type=primary (default)
    # .../?domain_type=secondary
    #
    # .../?view_type=bydomain (default)
    # .../?view_type=byip
]
