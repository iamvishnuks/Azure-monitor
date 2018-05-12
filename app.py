import os
from flask import render_template, Flask, jsonify, request, redirect, flash, url_for
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)

import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from azure.mgmt.storage import StorageManagementClient

from msrestazure.azure_exceptions import CloudError

LOCATION = 'southindia'

def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

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
      vm_statuses.append({'name':vm.name,'status':status})
  count_run=0
  count_stop=0
  for vm in vm_statuses:
    if vm['status'] == 'running':
       count_run = count_run + 1
    if vm['status'] == 'deallocated':
       count_stop = count_stop + 1
  response = {'vm_running':count_run,'vm_stopped':count_stop,'vm_statuses':vm_statuses}
  return response

def get_storage_details():
  credentials, subscription_id = get_credentials()
  storage_client = StorageManagementClient(credentials, subscription_id)
  storage_accnts = [] 
  for item in storage_client.storage_accounts.list():
    storage_accnts.append(item.name)
  n = len(storage_accnts)
  response = {'storage_accounts':storage_accnts,'number':n}
  return response

@app.route('/storage')
def get_storage_info():
  return jsonify(get_storage_details())


@app.route('/vms')
def get_vm_statuses():
  return jsonify(get_vm_details())
  
@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
