from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from .views import records, domains, domain_records, rundeck_nodes_by_domain

urlpatterns = [
    ###
    ### PowerDNS API: Get info of all records at Domain
    ###
    # /api/powerdns/domains/
    url(r'domains/$',
        domains, name='domains'),
    # /api/powerdns/domain/1/records/
    url(r'domain/(?P<domain_id>[0-9]+)/records/$',
        domain_records, name='records_by_domain_id'),
    # /api/powerdns/domain/1/records/type/CNAME
    url(r'domain/(?P<domain_id>[0-9]+)/records/type/(?P<record_type>[a-zA-Z]+)/$',
        domain_records, name='records_by_domain_id_type'),
    # /api/powerdns/domain/domain.com/records/
    url(r'domain/(?P<domain_name>[a-zA-Z0-9\.]*)/records$',
        domain_records, name='records_by_domain_name'),
    # /api/powerdns/domain/domain.com/records/type/CNAME
    url(r'domain/(?P<domain_name>[a-zA-Z0-9\.]*)/records/type/(?P<record_type>[a-zA-Z]+)/$',
        domain_records, name='records_by_domain_name_type'),

    ###
    ### PowerDNS API: Get info of a specific Records
    ###
    # /api/powerdns/record/1
    url(r'record/(?P<record_id>[0-9]+)/$',
        records, name='record_by_id'),
    # /api/powerdns/record/record.domain.com
    url(r'records/(?P<record_name>[a-zA-Z0-9\.]*)/$',
        records, name='record_by_name'),
    # /api/powerdns/records/record.domain.com/type/A
    url(r'records/(?P<record_name>[a-zA-Z0-9\.]*)/type/(?P<record_type>[a-zA-Z]+)/$',
        records, name='records_by_name_type'),

    ###
    ### Rundeck API: List all Records at Domain like Rundeck JSON Format
    ###
    # /api/powerdns/rundeck_nodes/1
    url(r'rundeck_nodes/(?P<domain_id>[0-9]+)/$',
        rundeck_nodes_by_domain, name='rundeck_nodes_by_domain_id'),
    # /api/powerdns/rundeck_nodes/domain.com
    url(r'rundeck_nodes/(?P<domain_name>[a-zA-Z0-9\.]*)/$',
        rundeck_nodes_by_domain, name='rundeck_nodes_by_domain_name'),

]
