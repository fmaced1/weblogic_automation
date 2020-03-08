import time
import getopt
import sys
import re

"""
https://www.middlewareinventory.com/blog/weblogic-wlst-storeuserconfig-security-best-practice/
https://www.middlewareinventory.com/blog/weblogic-start-all-managed-servers-wlst-script/
"""

def conn():
        connect(USERNAME, PASSWORD, ADMINURL)

def usage():
        toprint = '''
========================================================================================================================================
------------------------------------------------------
TO CUSTOMIZE KEYFILE AND CONFIGFILE CREATION LOCATION
------------------------------------------------------
java weblogic.WLST storeuserconfig.py -u <value> -p <value> -c <value> -k <value> -a <adminurl>
                                {or}
java weblogic.WLST storeuserconfig.py --username=<value> --password=<value> --configfile=<value> --keyfile=<value> --adminurl=<value>
Here
-u represents "username"
-p represents "password"
-c represents "configfile"
-k represents "keyfile"
-a represents "adminurl"
--------
Example:
--------
java weblogic.WLST storeuserconfig.py -u weblogic -p weblogic1 -c /tmp/weblogic_configfile.secure -k /tmp/weblogic_keyfile.secure -a t3://localhost:17001
========================================================================================================================================
------------------------------------------------------
TO CREATE KEYFILE, CONFIGFILE IN DEFAULT LOCATION
------------------------------------------------------
Note*: This will create a configfile and keyfile in the home location of current user
java weblogic.WLST storeuserconfig.py --default -u <value> -p <value> -a <adminurl>
                                {or}
java weblogic.WLST storeuserconfig.py --default --username=<value> --password=<value> --adminurl=<value>
Here
--default represents "default" switch
-u represents "username"
-p represents "password"
-a represents "adminurl"
--------
Example:
--------
java weblogic.WLST storeuserconfig.py --default -u weblogic -p weblogic1 -a t3://localhost:17001
=======================================================================================================================================
        '''
        print toprint


def store_custom():
        storeUserConfig(CONFIGFILE,KEYFILE)


def store_default():
        storeUserConfig()


# MAIN
try:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:p:c:k:a:", ["username=", "password=", "configfile=","keyfile=", "help", "adminurl=", "default"])
except getopt.GetoptError:
        print "ERROR: Aw! Snap Some error Occured"
        print "ERROR: Some Required Parameters and Key is missing, Please Read the Usage before executing"
        print "java weblogic.WLST storeuserconfig.py help "

        sys.exit(2)

DEFAULTFLAG = ""

for o, a in opts:
        if o == "-v":
                verbose = True
        if o in ("-d", "--default"):
                DEFAULTFLAG="ON"
        elif o in ("-h", "--help"):
                usage()
                sys.exit()
        elif o in ("-c", "--configfile") and (DEFAULTFLAG != "ON"):
                print "INFO: Config file set to =>",a
                CONFIGFILE=a
        elif o in ("-k", "--keyfile") and (DEFAULTFLAG != "ON"):
                print "INFO: Key file set to =>",a
                KEYFILE=a
        elif o in ("-u", "--username"):
                print "INFO: UserName set to =>",a
                USERNAME=a
        elif o in ("-p", "--password"):
                print "INFO: Password set to =>",a
                PASSWORD=a
        elif o in ("-a", "--adminurl"):
                print "INFO: AdminUrl set to =>",a
                ADMINURL=a
                match = re.match(r'(t3|t3s)(\:)(\/\/)(.*:)(\d+)', ADMINURL)
                if not match:
                        print "\nERROR: AdminURL is wrong, Make sure you are using t3/t3s protocol"
                        print "Sample AdminURL: t3://localhost:17001"
                        sys.exit()
        else:
                assert False, "ERROR: Option is not supported"
                sys.exit()

try:
        if (DEFAULTFLAG != "ON"):
                if (CONFIGFILE and KEYFILE and USERNAME and PASSWORD and ADMINURL):
                        print "\nINFO: Values have been set properly"
                        conn()
                        store_custom()
                else:
                        print "\nERROR: Some Essential Keys are missing";
        else:
                if (USERNAME and PASSWORD and ADMINURL):
                        print "\nValues have been set properly"
                        conn()
                        store_default()
                else:
                        print "\nERROR: Some Essential Keys are missing";
                        usage()
except:
        print "\nERROR: Got Some Error! Please make sure you are executing the script right",sys.exc_info()[0]
        usage()