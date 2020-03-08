https://github.com/oracle/docker-images/tree/master/OracleWebLogic
 
sudo useradd oracle
sudo passwd oracle
su oracle
cd ~

"Step 1 - Docker"
sudo yum install git
sudo yum update && yum install yum-utils
sudo yum remove docker docker-common docker-selinux docker-engine
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum makecache fast
sudo yum install docker-ce
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker oracle
 
"Step 2 - Oracle Images"
        Oracle Docker Images: https://github.com/oracle/docker-images
 
mkdir -p ~/lab_weblogic/oracle; cd ~/lab_weblogic/oracle
git clone https://github.com/oracle/docker-images.git
 
"Fazer download e colocar no diretorio ~/lab_weblogic/oracle"
WebLogic: https://www.oracle.com/technetwork/middleware/fusion-middleware/downloads/index.html
Java Jre8: https://www.oracle.com/technetwork/java/javase/downloads/server-jre8-downloads-2133154.html
scp ~/Download/? nagios@192.168.15.13:/home/nagios/lab_weblogic/oracle
 
"Step 3 - Build Java Jre"
cd ~/lab_weblogic/oracle/docker-images/OracleJava/java-8
cp ~/lab_weblogic/oracle/server-jre-8u191-linux-x64.tar.gz .
./build.sh
 
"Step 4 - Build WebLogic"
cd ~/lab_weblogic/oracle/docker-images/OracleWebLogic/dockerfiles/
cp ~/lab_weblogic/oracle/fmw_12.2.1.3.0_wls_quick_Disk1_1of1.zip  12.2.1.3/
./buildDockerImage.sh 12.2.1.3 -d
 
"Step 5 - Build Domain"
cd ~/lab_weblogic/lab_weblogic/oracle/docker-images/OracleWebLogic/samples/12213-domain
./build.sh
 
"To start the containerized Administration Server, run:"
docker run -d --name=wlsadmin --hostname=wlsadmin -p 7001:7001 --env-file ./container-scripts/domain.properties -e ADMIN_PASSWORD=WebLogic123 12213-domain
docker ps |grep domain|cut -d" " -f1|xargs docker logs
 
http://192.168.15.13:7001/console
User: weblogic
WebLogic123
 
"To start a containerized Managed Server (MS1) to self-register with the Administration Server above, run:"
docker run -d --name MS1 --link wlsadmin:wlsadmin -p 8001:8001 --env-file ./container-scripts/domain.properties -e ADMIN_PASSWORD=WebLogic123 -e MS_NAME=MS1 --volumes-from wlsadmin 12213-domain createServer.sh
 
"To start a second Managed Server (MS2), run:"
docker run -d --name MS2 --link wlsadmin:wlsadmin -p 8002:8001 --env-file ./container-scripts/domain.properties -e ADMIN_PASSWORD=WebLogic123 -e MS_NAME=MS2 --volumes-from wlsadmin 12213-domain createServer.sh

docker exec -it wlsadmin /bin/bash

usermod -aG root oracle