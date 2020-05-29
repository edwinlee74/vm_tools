'''
Purpose: To check status of ESXI or vCenter server. 
Description: A tool is similar to the vmwarevSphereHealthCheck.pl that 
             will generate a report.
'''
from pyVim.connect import SmartConnect, Disconnect
import argparse
import atexit
import ssl
import sys

def get_args():
    parser = argparse.ArgumentParser(description=
            'To gererate a report for vSphere health check.')
    parser.add_argument('--server',dest='server',type=str,
            help='The server that you want to connect to.')
    parser.add_argument('--username',dest='username',type=str,
            help='The username that you want to login on.')
    parser.add_argument('--password',dest='password',type=str,
            help='The password that you want to login on.')
    parser.add_argument('--port',dest='port',default=443,type=int,
			help='The port you connect to.')
    if len(sys.argv)==1:
       parser.print_help(sys.stderr)
       sys.exit(1)

    args = parser.parse_args()
    return args

def get_content(server,username,password,port):
    '''return si object after connection.'''
    context = None
    if hasattr(ssl, '_create_unverified_context'):
       context = ssl._create_unverified_context()
    try:
        si = SmartConnect(host=server,
                          user=username,
                          pwd=password,
                          port=port,
                          sslContext=context)
    except Exception as error:
        print(f'Can not connect to server.\n\nReason: {error}')
        sys.exit(1)

    atexit.register(Disconnect,si)
    content = si.RetrieveContent()
    return content

def get_about_info(content):
    about_info = {
        'name': content.about.name,
        'fullName': content.about.fullName,
        'version': content.about.version,
        'build': content.about.build,
        'apiType': content.about.apiType,
        'apiVersion': content.about.apiVersion,
        'productLineId': content.about.productLineId,
        'instanceUuid': content.about.instanceUuid
    }
    return about_info

def get_license_info(content):
    license = []
    feature = []
    for item in content.licenseManager.licenses:
        lic = {'lic_key': item.licenseKey, 'name': item.name, 
                'total': item.total, 'used': item.used, 
                'cost_unit': item.costUnit}
        license.append(lic)
        for fet in item.properties:
            if fet.key == 'feature':
                feature.append(fet.value.value)
    return license, feature
    
def get_plugin_info(content):
    '''Get plugin info only from vcenter.'''

    plugin = []
    for item in content.extensionManager.extensionList:
        plg = {'name': item.description.label, 'version': item.version,
                'summary': item.description.summary, 
                'company': item.company}
        plugin.append(plg)
    return plugin

def get_vpx_setting(content):
    '''vcenter setting'''
    setting = []
    for item in content.setting.setting:
        setting.append({item.key:item.value})
    return setting

if __name__ == "__main__":  
    args = get_args()
    content = get_content(args.server,args.username,
		args.password,args.port)
    setting = get_vpx_setting(content)
    print(setting)

