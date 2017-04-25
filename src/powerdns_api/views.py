#from django.shortcuts import`: render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from powerdns_manager.models import Record, Domain

###
### JSON Serializers
###
def serialize_dns_domains():
    data = {}
    for domain_obj in Domain.objects.all():
        data[domain_obj.name] = {
            "id": domain_obj.id,
            "type": domain_obj.type }
    return data

def serialize_dns_records(queryset_filter):
    data = {}
    for record_obj in Record.objects.filter(**queryset_filter):
        if not record_obj.name in data.keys(): 
            data[record_obj.name] = {}
        if not record_obj.type in data[record_obj.name].keys():
            data[record_obj.name][record_obj.type] = []
        data[record_obj.name][record_obj.type] += [{
            "id": record_obj.id,
            "content": record_obj.content,
            "ttl": record_obj.ttl }]
    return data

def serialize_rundeck_node(queryset_filter):
    data = {}
    for record_obj in Record.objects.filter(**queryset_filter):
        data[record_obj.name] = {
            "nodename": record_obj.name,
            "hostname": record_obj.content,
            "username": "orquestrador",
            "description": "(Record type: "+record_obj.type+") Node exported from powerDNS",
            "tags": "vistosystem_dev" } 
    return data

###
### API VIEWS
###
def domains(request):
    json_dict = serialize_dns_domains()
    return JsonResponse(json_dict)

def records(request, record_id=None, record_name=None, record_type=None):
    queryset_filter = {}

    if record_id != None:
        queryset_filter['id'] = record_id
    elif record_name != None:
        queryset_filter['name'] = record_name
    else:
        raise HttpResponseBadRequest('{"error": "This endpoint requires (record_id or record_name) params to properly works"}')
        
    if record_type != None and record_type != 'ANY':
        queryset_filter['type'] = record_type

    json_dict = serialize_dns_records(queryset_filter)
    return JsonResponse(json_dict, json_dumps_params={'sort_keys':True})
  

def domain_records(request, domain_id=None, domain_name=None, record_type=None):
    queryset_filter = {}

    if domain_id != None:
        queryset_filter['domain_id'] = domain_id
    elif domain_name != None:
        queryset_filter['domain__name'] = domain_name
    else:
        raise HttpResponseBadRequest('{"error": "This endpoint requires (domain_id or domain_name) params to properly works"}')
        
    if record_type != None:
        queryset_filter['type'] = record_type

    json_dict = serialize_dns_records(queryset_filter)
    return JsonResponse(json_dict, json_dumps_params={'sort_keys':True})



def rundeck_nodes_by_domain(request, domain_id=None, domain_name=None):
    queryset_filter = {'type':'A'}

    if domain_id != None:
        queryset_filter['domain_id'] = domain_id
    elif domain_name != None:
        queryset_filter['domain__name'] = domain_name
    else:
        raise HttpResponseBadRequest('{"error": "This endpoint requires (domain_id or domain_name) params to properly works"}')
        
    json_dict = serialize_rundeck_node(queryset_filter)
    return JsonResponse(json_dict, json_dumps_params={'sort_keys':True})
