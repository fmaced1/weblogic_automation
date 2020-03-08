import sys
import re
import getopt

def usage():
        toprint = '''
---------------------------------------------------------
Invoke the script using any one of the following command
---------------------------------------------------------
java weblogic.WLST managedServersStart.py -u weblogic -p weblogic1 -a t3://localhost:7001
(or)
java weblogic.WLST managedServersStart.py -c /app/oracle/WebLogicService/weblogic_configfile.secure -k /app/oracle/WebLogicService/weblogic_keyfile.secure -a t3://localhost:7001
---------------------------------------------------------
        '''
        print toprint

def connectt():
        connect(USERNAME, PASSWORD, ADMINURL)


def connect_secure():
        connect(userConfigFile=CONFIGFILE,userKeyFile=KEYFILE,url=ADMINURL)


def getdomainstatus():
        servers=cmo.getServers()
        print "-------------------------------------------------------"
        print "\t"+cmo.getName()+" domain current status"
        print "-------------------------------------------------------"
        for server in servers:
                status=state(server.getName(),server.getType())
        print "-------------------------------------------------------"


# Start the servers which are down
def startmanagedservers(ManagedServersList):
        servers=cmo.getServers()
        domainRuntime()
        for server in servers:
                for MS in ManagedServersList.split(','):
                        if server.getName() == MS:
                                bean="/ServerLifeCycleRuntimes/"+server.getName()
                                serverbean=getMBean(bean)
                                #print "serverbean",serverbean
                                print "Current status of the server",server.getName(),"is",serverbean.getState()
                                if serverbean.getState() == 'SHUTDOWN' or serverbean.getState() == 'FAILED_NOT_RESTARTABLE' or serverbean.getState() == 'UNKNOWN':
                                        print "Starting the servers which are in SHUTDOWN and FAILED_NOT_RESTARTABLE status"
                                        print " --> Starting the Server ",server.getName()
                                        try:
                                                start(server.getName(),server.getType())
                                        except:
                                                dumpStack()
                                                pass

CONFIGFILE="NULL"
KEYFILE="NULL"
USERNAME="NULL"
PASSWORD="NULL"
ADMINURL="NULL"
ManagedServersList="NULL"
DOWNSERVERS=[]

if len(sys.argv) < 3:
        print "Invalid Number of arguments, Expected 4 arguments, Found [%d]"%(len(sys.argv))
        print ""

try:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:p:c:k:a:f:s:", ["username=", "password=", "configfile=","keyfile=", "help", "adminurl=", "managedserverslist=", "status="])
except getopt.GetoptError:
        print "Option is not valid"
        usage();
        sys.exit(2)


for o, a in opts:
        if o in ("-h", "--help"):
                usage()
                sys.exit()
        elif o in ("-c", "--configfile"):
                print "INFO: Config file set to =>",a
                CONFIGFILE=a
        elif o in ("-k", "--keyfile"):
                print "INFO: Key file set to =>",a
                KEYFILE=a
        elif o in ("-u", "--username"):
                print "INFO: UserName set to =>",a
                USERNAME=a
        elif o in ("-p", "--password"):
                print "INFO: Password set to => ****"
                PASSWORD=a
        elif o in ("-s", "--status"):
                GETSTATUS="NULL"
                GETSTATUS=a
        elif o in ("-a", "--adminurl"):
                print "INFO: AdminUrl set to =>",a
                ADMINURL=a
                match = re.match(r'(t3|t3s)(\:)(\/\/)(.*:)(\d+)', ADMINURL)
                if not match:
                        print "\nERROR: AdminURL is wrong, Make sure you are using t3/t3s protocol"
                        print "Sample AdminURL: t3://localhost:17001"
                        sys.exit()
        elif o in ("-f", "--managedserverslist"):
                print "INFO: ManagedServersList set to =>",a
                ManagedServersList=a
        else:
                assert False, "ERROR: Option is not supported"
                sys.exit()

if USERNAME.find("NULL") >= 0 and PASSWORD.find("NULL") >= 0 and KEYFILE.find("NULL") >= 0 and CONFIGFILE.find("NULL") >= 0:
        print "The Script must be started with username, password and ManagedServersList for AdminServer (or) Keyfile, configfile and ManagedServersList"
        usage()
        sys.exit()

if ADMINURL == "NULL":
        print "AdminURL is empty",ADMINURL
        usage()
        sys.exit();

from java.io import FileInputStream

propInputStream = FileInputStream(ManagedServersList)
configProps = Properties()
configProps.load(propInputStream)

# Set all variables from values in config file.
ManagedServersList=configProps.get("config.managedservers")

# Display the variable values.
print('')
print('--------------------')
print('Managed Servers List')
print(ManagedServersList)
print('--------------------')
print('')

if GETSTATUS == "TRUE" and CONFIGFILE and KEYFILE:
        connect_secure();
        getdomainstatus();
elif CONFIGFILE and KEYFILE:
        connect_secure();
        getdomainstatus();
        startmanagedservers(ManagedServersList)
else:
        connectt();
        getdomainstatus();
        startmanagedservers(ManagedServersList)