import atexit
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import time
import datetime
from pyVmomi import vmodl
from threading import Thread
import ssl
from vmwareSamples.samples.tools import tasks


#-------Operation Flags-----------#

vms_flag = False
hosts_flag  = True

def powerOnVMs(children):
    for vm in children:
        if vm.runtime.powerState == 'poweredOff':
            print('-----------------------------------')
            print("Script will Power on " + vm.name)
            print('===================================')
            vm.PowerOnVM_Task()

def Hosts(si, children):
    for host in children:
        connectionState = host.runtime.connectionState
        if connectionState == 'disconnected':
            print('Host Connection State: ' + connectionState)
            print('Script trying to connect host:' + host.name)
            print("Reconnecting.............")
            try:
                task = host.ReconnectHost_Task()
                
            except:
                print('failed to reconnect....!')
            tasks.wait_for_tasks(si, [task])
            validate = host.runtime.connectionState
            print(validate)

    return 1


context = None
if hasattr(ssl, '_create_unverified_context'):
    context = ssl._create_unverified_context()
si = SmartConnect(
    host='192.168.1.50',user='administrator@vsphere.local',pwd='P@ssw0rd', sslContext=context)
content = si.RetrieveContent()

container = content.rootFolder
vmsViewType = [vim.VirtualMachine]
hostsViewType = [vim.HostSystem]
recursive = True

vmsContainer = content.viewManager.CreateContainerView(container, vmsViewType, recursive)
hostsContainer = content.viewManager.CreateContainerView(container, hostsViewType, recursive)
vms = vmsContainer.view
hosts = hostsContainer.view

# if vms_flag == True:
#     powerOnVMs(vms)

if hosts_flag == True:
    host_return = Hosts(si, hosts)

    if host_return == 1:
        powerOnVMs(vms)
else:

    print("Nothing to do... please check script flags")

