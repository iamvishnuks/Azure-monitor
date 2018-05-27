import datetime,os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

vm_name = 'dev3'
resource_group_name = "r1"
def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

credentials, subscription_id = get_credentials()

def get_vm_details():
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
      vm_statuses.append({'name': vm.name, 'status': status})
  count_run = 0
  count_stop = 0
  count_deallocated = 0
  for vm in vm_statuses:
    if vm['status'] == 'running':
       count_run = count_run + 1
    elif vm['status'] == 'deallocated':
       count_deallocated = count_deallocated + 1
    elif vm['status'] == 'stopped':
       count_stop = count_stop + 1
  response = {'vm_running': count_run, 'vm_stopped': count_stop, 'vm_deallocated': count_deallocated, 'vm_statuses': vm_statuses}
  print allvms
  return allvms


allvms=get_vm_details()

for i in allvms:
  resource_id = (
      "subscriptions/{}/"
      "resourceGroups/{}/"
      "providers/Microsoft.Compute/virtualMachines/{}"
  ).format(subscription_id, resource_group_name, i)

# create client
  client = MonitorManagementClient(
      credentials,
      subscription_id
  )

# You can get the available metrics of this specific resource
  for metric in client.metric_definitions.list(resource_id):
      # azure.monitor.models.MetricDefinition
      print("{}: id={}, unit={}".format(
          metric.name.localized_value,
          metric.name.value,
          metric.unit
      ))

# Get CPU total of yesterday for this VM, by hour
  today = datetime.datetime.now().date()
  yesterday = today - datetime.timedelta(days=1)
  metrics_data = client.metrics.list(
      resource_id,
      timespan="{}/{}".format(yesterday, today),
      interval='PT1H',
      metric='Percentage CPU',
      aggregation='Total'
  )
  for item in metrics_data.value:
      # azure.mgmt.monitor.models.Metric
      print("{} ({})".format(item.name.localized_value, item.unit.name))
      for timeserie in item.timeseries:
          for data in timeserie.data:
              # azure.mgmt.monitor.models.MetricData
              print("{}: {}".format(data.time_stamp, data.total))

