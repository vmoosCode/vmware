from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import argparse
import atexit
import getpass
import ssl
import subprocess


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host')
    args = parser.parse_args()
    return args

def get_thumprint(host):
    p1 = subprocess.run(
        'echo -n | openssl s_client -connect 192.168.1.51:443 |& openssl x509  -fingerprint -sha1 -noout ', shell=True, stdout=subprocess.PIPE)
    sha1 = p1.stdout.decode()


    out = sha1.split(b'=')[-1].strip()
    print(out)
    return sha1
    

def get_ssl_thumbprint(host_ip):
    p1 = subprocess.Popen(
        ('echo-n'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(('openssl openssls_client', '-connect', '{0}:443'.format(
        host_ip)), stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(('opensslx509', '-noout', '-fingerprint', '-sha1'),
                          stdin=p2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p3.stdout.read()
    ssl_thumbprint = out.split(b'=')[-1].strip()
    return ssl_thumbprint.decode("utf-8")
    
def buildDC(name, si):
    folder = si.content.rootFolder
    if len(name) > 79:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")
    dc = folder.CreateDatacenter(name)

def create_cluster(name, si, dcname):
    content = si.RetrieveContent()
    datacenters = content.rootFolder.childEntity
    conf_spec = vim.cluster.ConfigSpec()
    for dc in datacenters:  
        if dcname in dc.name:
            cluster = dc.hostFolder.CreateCluster(name, conf_spec)
            host_connect_spec = vim.host.ConnectSpec()  
            host_connect_spec.hostName = '192.168.1.51'
            host_connect_spec.userName = 'root'
            host_connect_spec.password = 'password'
            host_connect_spec.force = True
            host_connect_spec.sslThumbprint = get_thumprint('192.168.1.51')
            add_host_task = cluster.AddHost_Task(
                spec=host_connect_spec, asConnected=True)
            # tasks.wait_for_tasks(si, [add_host_task])"
            print("Cluster and host created successfully")
            




def main():
    """
    Simple command-line program for listing the  virtual machines on a system.
    """

    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and '
                                        'user %s: ' % (args.host, args.user))

    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
    si = SmartConnect(host=args.host,
                        user=args.user,
                        pwd=password,
                        port=int(args.port),
                        sslContext=context)
    if not si:
        print("Could not connect to the specified host using specified "
                "username and password")
        return -1


    
    # create_cluster('cluster1',si,'new_DC')

    get_thumprint('192.168.1.51')

    
    
    atexit.register(Disconnect, si)



# Start program
if __name__ == "__main__":
    main()
