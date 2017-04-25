from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from .models import Environment, Node, SSHUser


# JSON Serializers
def serialize_rundeck_node(queryset_filter, domain_type, view_type):
    # ensure domain_type for primary or secondary
    if domain_type != 'secondary':
        domain_type = 'primary'

    data = {}
    for node_obj in Node.objects.filter(**queryset_filter):

        # get domain obj based on primary or secondary domain
        domain_obj = getattr(node_obj.env, '{}_domain'.format(domain_type))
        if view_type != 'byip':
            # build fqdn of node and return as node_address
            hostname = '{}.{}'.format(node_obj.name, domain_obj.name)
        else:
            # get node address based on primary or secondary domain
            hostname = getattr(node_obj, '{}_address'.format(domain_type))
        # short desc
        if node_obj.desc:
            node_obj.desc = node_obj.desc[:30]

        data[node_obj.name] = {
            "nodename": node_obj.name,
            "hostname": hostname,
            "username": node_obj.ssh_specific_user.login,
            "description": node_obj.desc,
            "tags": ','.join(node_obj.tags.values_list('name', flat=True)),
        }
    return data


# Rundeck View
def save_nodes(request, env_name, node_name, address, user_name):

    node = Node(env=Environment.objects.get(name=env_name), name=node_name, primary_address=address,
              ssh_specific_user=SSHUser.objects.get(login=user_name))
    node.save()
    return JsonResponse(node)

def rundeck_nodes_by_env(request, env_id=None, env_name=None):
    if request.GET.get('domain_type') and request.GET['domain_type'] == 'secondary':
        domain_type = 'secondary'
    else:
        domain_type = 'primary'

    if request.GET.get('view_type') and request.GET['view_type'] == 'byip':
        view_type = 'byip'
    else:
        view_type = 'bydomain'

    queryset_filter = {}

    if env_id is not None:
        queryset_filter['env__id'] = env_id
    elif env_name is not None:
        queryset_filter['env__name'] = env_name
    else:
        raise HttpResponseBadRequest(
            '{"error": "This endpoint requires (env_id or env_name) params to properly works"}')

    json_dict = serialize_rundeck_node(queryset_filter, domain_type, view_type)
    return JsonResponse(json_dict, json_dumps_params={'sort_keys': True})
