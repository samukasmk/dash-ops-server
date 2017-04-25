from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from powerdns_manager.models import Domain as PowerDnsDomain
from powerdns_manager.models import Record as PowerDnsRecord
from .exceptions import NodeEnvIsNone, DomainEnvIsNone

ADDRESS_TYPE = (
    (1, 'A'),
    (2, 'CNAME')
)


class Environment(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    primary_domain = models.OneToOneField(PowerDnsDomain, unique=True,
        null=False, blank=False, related_name='env_as_primary_domain')
    secondary_domain = models.OneToOneField(PowerDnsDomain, unique=True,
        null=True, blank=True, related_name='env_as_secondary_domain')

    def __str__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    env = models.ForeignKey('Environment', null=False, blank=False,
        verbose_name='environment')
    desc = models.TextField(max_length=500, null=True, blank=True,
        verbose_name='description')
    ssh_specific_user = models.ForeignKey('SSHUser', null=False, blank=False)
    primary_address = models.CharField(max_length=200, null=False, blank=False)
    primary_address_type = models.IntegerField(choices=ADDRESS_TYPE, default=1,
        null=False, blank=False)
    secondary_address = models.CharField(max_length=200, null=True, blank=True)
    secondary_address_type = models.IntegerField(choices=ADDRESS_TYPE, default=1,
        null=True, blank=True)
    tags = models.ManyToManyField('NodeTag', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'env',)

    def save(self, *args, **kwargs):
        if self.env is None:
            raise NodeEnvIsNone('Node has no associated object Environment' +
                'at field env')

        try:
            if self.env.primary_domain:
                create_powerdns_record(
                    domain_obj=self.env.primary_domain,
                    node_name=self.name,
                    node_address=self.primary_address,
                    node_address_type=self.primary_address_type)
        except ObjectDoesNotExist:
            raise DomainEnvIsNone('Environment has no primary_domain ' +
                'associated to object powerdns_manager.models.Domain')

        super(Node, self).save(*args, **kwargs)

        try:
            if self.env.secondary_domain:
                create_powerdns_record(
                    domain_obj=self.env.secondary_domain,
                    node_name=self.name,
                    node_address=self.secondary_address,
                    node_address_type=self.secondary_address_type)
        except ObjectDoesNotExist:
            pass


class NodeTag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class SSHUser(models.Model):
    login = models.CharField(max_length=100, unique=True, null=False, blank=False)

    def __str__(self):
        return self.login


def create_powerdns_record(domain_obj, node_name, node_address, node_address_type):
    # define FQDN of record
    record_name = node_name + '.' + domain_obj.name
    # select record type from CHOICES tuple
    record_type = {k: v for k,v in ADDRESS_TYPE}[node_address_type]
    # remove all record objs with specific FQDN
    PowerDnsRecord.objects.filter(name=record_name).delete()
    # create record object
    PowerDnsRecord.objects.create(
        type=record_type,
        name=record_name,
        ordername=node_name,
        content=node_address,
        domain_id=domain_obj.id,
        auth=True)
