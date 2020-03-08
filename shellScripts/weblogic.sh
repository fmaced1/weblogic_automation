#!/bin/sh
#
# weblogic Start Oracle Weblogic
#
# chkconfig: 345 90 10
# description: Starts, stops weblogic service
#
# home: /app/oracle/WebLogicService/
#
######################
# Oracle - WebLogic #
######################
### BEGIN INIT INFO
# Provides: WebLogic
# Required-Start: $network $local_fs
# Required-Stop:
# Default-Start: 3 4 5
# Default-Stop: 0 1 2 6
# Description: Script to start NodeManager, AdminServer and ManagedServers
### END INIT INFO


CONFIG_FILES=/app/oracle/WebLogicService/configFiles
source $CONFIG_FILES/config.startWebLogic


getStatusNodeManager () {
        NM_STATUS_INT=""
        NM_STATUS_INT=`netstat -anp|grep "0\.0\.0\.0:555[5-6]"|grep -i java|awk '{ print$7 }'|cut -d"/" -f1|sort|uniq|wc -l`
        PID_NM=`netstat -anp|grep "0\.0\.0\.0:555[5-6]"|grep -i java|awk '{ print$7 }'|cut -d"/" -f1|sort|uniq`
}


getStatusAdminServer () {
        ADM_STATUS_INT=""
        ADM_STATUS_INT=`netstat -anp|grep ":7001"|grep "0\.0\.0\.0:\*"|grep -i java|awk '{ print$7 }'|cut -d"/" -f1|sort|uniq|wc -l`
        PID_ADM=`netstat -anp|grep ":7001"|grep "0\.0\.0\.0:\*"|grep -i java|awk '{ print$7 }'|cut -d"/" -f1|sort|uniq`
}


getStatusManagedServers () {
        setEnvAdminServer
        java weblogic.WLST $WLST_SCRIPTS/managedServersStart.py -c $WLST_ADMIN_KEYS/weblogic_configfile.secure -k $WLST_ADMIN_KEYS/weblogic_keyfile.secure -a t3://$(hostname):7001 -f "$CONFIG_FILES/config.managedservers" -s TRUE
}


printStatusNodeManager () {
        echo ""
        echo "-----------------------"
        echo "Looking for NodeManager"
        getStatusNodeManager
        if [ ${NM_STATUS_INT} -ge 1 ];then
                NM_STATUS="RUNNING"
        else
                NM_STATUS="DOWN"
        fi
        echo "NodeManager Status: ${NM_STATUS_INT} - $PID_NM - $NM_STATUS"
        echo "-----------------------"
        echo ""
}


printStatusAdminServer () {
        echo ""
        echo "-----------------------"
        echo "Looking for AdminServer"
        getStatusAdminServer
        if [ ${ADM_STATUS_INT} -ge 1 ];then
                ADM_STATUS="RUNNING"
        else
                ADM_STATUS="DOWN"
        fi
                echo "AdminServer Status: ${ADM_STATUS_INT} - $PID_ADM - $ADM_STATUS"
        echo "-----------------------"
        echo ""
}


printStatusManagedServers () {
        if [ ${AdminServerFlag} == "TRUE" ];then
                echo ""
                echo "Looking for ManagedServers"
                getStatusManagedServers
                echo ""
        else
                echo "The AdminServerFlag is not TRUE in $CONFIG_FILES/config.startWebLogic"
        fi
}


setEnvNodeManager () {
        if [ -e ${NodeManagerEnvFile} ];then
                echo ""
                echo "-----------------------"
                echo "Setting NodeManager Env"
                echo "-----------------------"
                . ${NodeManagerEnvFile} >/dev/null
        else
                echo ""
                echo "File not found: $NodeManagerEnvFile"
        fi
}


setEnvAdminServer () {
        if [ -e ${AdminServerEnvFile} ];then
                echo ""
                echo "-----------------------"
                echo "Setting AdminServer Env"
                echo "-----------------------"
                . ${AdminServerEnvFile} >/dev/null
        else
                echo ""
                echo "File not found: $AdminServerEnvFile"
        fi
}


startNodeManager () {
        echo ""
        echo "--------------------"
        echo "Starting NodeManager"
        echo "--------------------"
        if [ `id -u` == "0" ];then
                chown admweb.admweb -R /app/oracle/ /logs/oracle/
        fi
        nohup su admweb ${NodeManagerStartScript} >> ${NodeManagerDir}/nohup.out 2>&1 &
}


startAdminServer () {
        if [ `id -u` == "0" ];then
                chown admweb.admweb -R /app/oracle/ /logs/oracle/
        fi
        nohup su admweb ${AdminServerStartScript} >> ${AdminServerDir}/nohup.out 2>&1 &
}


startManagedServers () {
        echo ""
        echo "--------------------"
        echo "Starting ManagedServers"
        echo "--------------------"
        if [ ${AdminServerFlag} == "TRUE" ];then
                setEnvAdminServer
                echo "Waiting for console ... 60 seconds"
                counter=0
                while [ $counter -lt 20 ];do
                        counter=$((counter++))
                        if [ $(curl -sL --max-time 60 -w "%{http_code}\\n" "http://$(hostname):7001/console" -o /dev/null) == "200" ];then
                                java weblogic.WLST $WLST_SCRIPTS/managedServersStart.py -c $WLST_ADMIN_KEYS/weblogic_configfile.secure -k $WLST_ADMIN_KEYS/weblogic_keyfile.secure -a t3://$(hostname):7001 -f "$CONFIG_FILES/config.managedservers" -s FALSE
                                counter=20
                        else
                                echo "Console is DOWN http://$(hostname):7001/console"
                                echo "Sleeping 10 seconds ..."
                                sleep 10
                        fi
                done
        else
                echo "The AdminServerFlag is not TRUE in $CONFIG_FILES/config.startWebLogic"
        fi
}


stopNodeManager () {
        getStatusNodeManager
        echo ""
        echo "--------------------"
        echo "Killing NodeManager"
        echo "--------------------"
        echo "PID_NM: $PID_NM"
        echo $PID_NM|xargs skill -9
}


stopAdminServer () {
        getStatusAdminServer
        echo ""
        echo "--------------------"
        echo "Killing AdminServer"
        echo "--------------------"
        echo "PID_ADM: $PID_ADM"
        echo $PID_ADM|xargs skill -9
}


stopManagedServers () {
        getStatusManagedServers
        echo ""
        echo "--------------------"
        echo "Killing ManagedServers"
        echo "--------------------"
        echo "PID_MS: $PID_MS"
        echo $PID_MS|xargs skill -9
}


mainStartNodeManager () {
        setEnvNodeManager
        getStatusNodeManager


        if [ ${NM_STATUS_INT} -ge 1 ];then
                printStatusNodeManager
        else
                startNodeManager
                echo "Sleeping 10 seconds ..."
                sleep 10
                printStatusNodeManager
        fi
}


mainStartAdminServer () {
        echo ""
        echo "--------------------"
        echo "Starting AdminServer"
        echo "--------------------"
        if [ ${AdminServerFlag} == "TRUE" ];then
                setEnvAdminServer
                getStatusAdminServer


                if [ ${ADM_STATUS_INT} -ge 1 ];then
                        printStatusAdminServer
                else
                        startAdminServer
                        echo "Sleeping 10 seconds ..."
                        sleep 10
                        printStatusAdminServer
                fi
        else
                echo "The AdminServerFlag is not TRUE in $CONFIG_FILES/config.startWebLogic"
        fi
}


mainPrintStatus () {
        printStatusNodeManager
        printStatusAdminServer
        printStatusManagedServers
}


mainStopNodeManager () {
        setEnvNodeManager
        getStatusNodeManager


        if [ ${NM_STATUS_INT} -le 0 ];then
                printStatusNodeManager
        else
                stopNodeManager
                printStatusNodeManager
        fi
}


mainStopAdminServer () {
        getStatusAdminServer


        if [ ${ADM_STATUS_INT} -le 0 ];then
                printStatusAdminServer
        else
                stopAdminServer
                printStatusAdminServer
        fi
}


mainStopManagedServers () {
        echo "Function StopManagedServers are currently in development :)"
}


mainStopAdminServer () {
        setEnvAdminServer
        getStatusAdminServer


        if [ ${ADM_STATUS_INT} -le 0 ];then
                printStatusAdminServer
        else
                stopAdminServer
                printStatusAdminServer
        fi
}


case "$1" in
  start)
    mainStartNodeManager
    mainStartAdminServer
    startManagedServers
  ;;


  stop)
    mainStopNodeManager
    mainStopAdminServer
    mainStopManagedServers
  ;;


  status)
    mainPrintStatus
  ;;


  statusNM)
    printStatusNodeManager
  ;;


  statusADM)
    printStatusAdminServer
  ;;


  statusMS)
    printStatusManagedServers
  ;;


  stopNM)
    mainStopNodeManager
  ;;


  stopMS)
    mainStopManagedServers
  ;;


  stopADM)
    mainStopAdminServer
  ;;


  startMS)
    startManagedServers
  ;;


  startNM)
    mainStartNodeManager
  ;;


  startADM)
    mainStartAdminServer
  ;;


  envNM)
    setEnvNodeManager
  ;;


  envADM)
    setEnvAdminServer
  ;;


  *)
    echo "Usage: $0 {start|stop|status|statusADM|statusNM|statusMS|startNM|startADM|stopMS|startMS|stopNM|stopADM|envNM|envADM}"
    exit 1
  ;;


esac