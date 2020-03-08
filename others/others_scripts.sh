import sys
import os

from java.util import Properties

DOMAIN_HOME="/u01/oracle/user_projects/domains/abc_domain"

domainProps = Properties()
userConfigFile = sys.argv[2]
userKeyFile = sys.argv[3]

os.chdir("/u01/oracle/user_projects/domains/abc_domain")

def connnectToAdminServer():

         connUri = domainProps.getProperty('adminURL')
         currentcount = 0;
         adminServerIsRunning = 'false';

         while ((adminServerIsRunning=='false')  and (currentcount<30)):
               try:
                        print 'Connecting to the Admin Server ('+connUri+')';
                        connect(userConfigFile=userConfigFile,userKeyFile=userKeyFile,url=connUri);
                        print 'Connected';
                        adminServerIsRunning = 'true';
               except:
                        print 'AdminServer is (not yet) running. Will wait for 10sec.';
                        java.lang.Thread.sleep(10000);
                        currentcount = currentcount +1;

         if (adminServerIsRunning=='false'):
                print 'Could not connect to admin server - script will be exit !'
                exit();
                
================================

managedServers = cmo.getServers()
domainRuntime()
for server in managedServers:
    if server.getName() != 'AdminServer':
        serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
        print server.getName() + " is " + serverState
        if (serverState == "SHUTDOWN") or (serverState == "FAILED_NOT_RESTARTABLE"):
            print "Starting " + server.getName();
            start(server.getName(),'Server')
            serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
            print "Now " + server.getName() + " is " + serverState;

================================

managedServers = cmo.getServers()
domainRuntime()
for server in managedServers:
    if server.getName():
        serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
        print server.getName() + " is " + serverState

================================
         
servidores = cmo.getServers()
for s in servidores:
    managedserver_name = s.getName()
    if managedserver_name != 'AdminServer':
        managedserver_type = s.getType()
        if managedserver_type is 'Server':
            start(managedserver_name,'Server')
        if managedserver_type is 'Cluster':
            start(managedserver_name,'Cluster')
        managedserver_status = cmo.lookupServerLifeCycleRuntime(managedserver_name).getState()
        print("Name: %s Type: %s Status: %s" % (managedserver_name,managedserver_type,managedserver_status))

        domainRuntime()
        status = cmo.lookupServerLifeCycleRuntime('managedserver_name').getState()

================================
         
servidores = cmo.getServers()
domainRuntime()
for server in servidores:
    if server.getName() != 'AdminServer':
        serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
        print server.getName() + " is " + serverState
        if (serverState == "SHUTDOWN") or (serverState == "FAILED_NOT_RESTARTABLE"):
            print "Starting " + server.getName();
            start(server.getName(),'Server')
            serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
            print "Now " + server.getName() + " is " + serverState;