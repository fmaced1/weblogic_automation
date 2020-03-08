import os
# Set env variables to execute WLST
os.system('. /u01/oracle/wlserver/server/bin/./setWLSEnv.sh')
os.system('. /u01/oracle/user_projects/domains/abc_domain/bin/./setDomainEnv.sh')
os.system('cd /u01/oracle/user_projects/domains/abc_domain/')

class weblogicTool(object):

    weblogic_adminserver = 'AdminServer'
    weblogic_adminURL = 't3://localhost:7001'
    weblogic_user = '/u01/oracle/oracle-WebLogicConfig.properties'
    weblogic_pass = '/u01/oracle/oracle-WebLogicKey.properties'
    nodemanager_host = 'localhost'
    nodemanager_port = '5556'
    nodemanager_domainName = 'abc_domain'
    nodemanager_domainDir = '/u01/oracle/user_projects/domains/abc_domain'
    nodemanager_nmType = 'plain'

    def startNodeManager(self):
        nodeManagerStatus = self.getNodeManagerStatus()
        print(str(nodeManagerStatus))
        if (nodeManagerStatus != 1):
            try:
                self.printDelimiter('Starting Node Manager ...')
                startNodeManager()
            except:
                dumpStack()
                self.printDelimiterHeader('Failed to start Node Manager ...')

    def connect2NodeManager(self):
        self.printDelimiter('Connecting to Node Manager ...')
        nodeManagerStatus=None
        try:
            nmConnect(userConfigFile=self.weblogic_user, userKeyFile=self.weblogic_pass, host=self.nodemanager_host, port=self.nodemanager_port, domainName=self.nodemanager_domainName, domainDir=self.nodemanager_domainDir, nmType=self.nodemanager_nmType)
            nodeManagerStatus=1
        except:
            dumpStack()
            self.printDelimiterHeader('Failed to connect to Node Manager :(')
            nodeManagerStatus=0

        return nodeManagerStatus

    def startAdminServer(self):
        self.printDelimiter('Starting Admin Server ...')
        self.connect2NodeManager()
        try:
            nmStart(self.weblogic_adminserver)
        except:
            dumpStack()
            self.printDelimiterHeader('Failed to start Admin Server :(')

    def killNodeManager(self):
        self.printDelimiter('Killing NodeManager ...')
        try:
            stopNodeManager()
        except:
            dumpStack()
            self.printDelimiterHeader('Failed to kill Node Manager :(')

    def killAdminServer(self):
        self.printDelimiter('Killing Admin Server ...')
        self.connect2NodeManager()
        self.connect2AdminServer()
        try:
            shutdown(self.weblogic_adminserver,'Server','true',1000,force='true', block='true')
        except:
            dumpStack()
            self.printDelimiterHeader('Failed to kill Admin Server :(')

    def killAllEnv(self):
        self.printDelimiter('Killing All Servers ...')
        self.killAdminServer()
        self.killNodeManager()

    def connect2AdminServer(self):
        self.printDelimiter('Connecting Admin Server ...')
        try:
            connect(userConfigFile=self.weblogic_user,userKeyFile=self.weblogic_pass,url=self.weblogic_adminURL)
        except:
            dumpStack()
            self.printDelimiterHeader('Failed to connect to Admin Server :(')

    def startManagedServers(self):
        self.printDelimiter('Starting All Managed Servers ...')
        self.connect2NodeManager()
        self.connect2AdminServer()
        managedServers = cmo.getServers()
        domainRuntime()
        for server in managedServers:
            if server.getName() != 'AdminServer' and server.getType() is 'Cluster':
                serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
                print server.getType() + ' ' + server.getName() + " is " + serverState
                if (serverState == "SHUTDOWN") or (serverState == "FAILED_NOT_RESTARTABLE"):
                    print "Starting " + ' ' + server.getType() + ' ' + server.getName();
                    start(server.getName(),server.getType())
                    serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
                    print "Now " + ' ' + server.getType() + ' ' + server.getName() + " is " + serverState;

        #TODO improve this function
        for server in managedServers:
            if server.getName() != 'AdminServer' and server.getType() is 'Server':
                serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
                print server.getType() + ' ' + server.getName() + " is " + serverState
                if (serverState == "SHUTDOWN") or (serverState == "FAILED_NOT_RESTARTABLE"):
                    print "Starting " + ' ' + server.getType() + ' ' + server.getName();
                    start(server.getName(),server.getType())
                    serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
                    print "Now " + ' ' + server.getType() + ' ' + server.getName() + " is " + serverState;

    def getNodeManagerStatus(self):
        self.printDelimiter('Getting Status - Node Manager ...')
        nodeManagerStatus=self.connect2NodeManager()
        if nodeManagerStatus:
            if (nodeManagerStatus == 1):
                print('NodeManager is RUNNING')
            elif (nodeManagerStatus == 0):
                print('NodeManager is DOWN !!!')
                nodeManagerStatus=0
        return nodeManagerStatus

    def getManagedServersStatus(self):
        self.printDelimiterHeader('Getting Status - Managed Servers ...')
        self.connect2NodeManager()
        self.connect2AdminServer()
        managedServers = cmo.getServers()
        domainRuntime()
        self.printDelimiterHeader('Status - Managed Servers')
        for server in managedServers:
            if server.getName():
                serverState = cmo.lookupServerLifeCycleRuntime(server.getName()).getState()
                print(str(server.getType() + " " + server.getName() + " is " + serverState))

    def printDelimiter(self, printable):
        print('')
        print(str('=' * 30 +'>_ '+ printable))

    def printDelimiterHeader(self, printable):
        print('')
        print(str('=' * 10 +'>_ '+ printable))

    def startWebLogicEnvironment(self):
        self.startNodeManager()
        self.getNodeManagerStatus()
        self.startAdminServer()
        self.startManagedServers()
        self.getManagedServersStatus()

wl = weblogicTool()
#wl.startWebLogicEnvironment()
#wl.killAllEnv()
#wl.startWebLogicEnvironment()
wl.startWebLogicEnvironment()