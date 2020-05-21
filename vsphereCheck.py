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

if __name__ == "__main__":  
    args = get_args()
    content = get_content(args.server,args.username,
		args.password,args.port)
    print(content)

    

