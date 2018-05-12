import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

from msrestazure.azure_exceptions import CloudError

LOCATION = 'southindia

def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


credentials, subscription_id = get_credentials()
resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)
allvms=[]
rgs = []
for rg in resource_client.resource_groups.list():
  rgs.append(rg.name)

for i in compute_client.virtual_machines.list_all():
  allvms.append(i.name)

vm_statuses = []

for rg in rgs:
  for i in allvms:
    vm = compute_client.virtual_machines.get(rg, i, expand = 'instanceview')
    status = vm.instance_view.statuses[1].code.split('/')[1]
    vm_statuses.append({'name':vm.name,'status':status})



