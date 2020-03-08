from java.io import FileInputStream

propInputStream = FileInputStream("user.properties.config")
configProps = Properties()
configProps.load(propInputStream)

hosts=configProps.get("admin.hosts")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")
realmName=configProps.get("security.realmName")

totalGroups=configProps.get("total.groups")
totalUsers_to_Create=configProps.get("total.username")

for server in hosts.split(','):
        adminURL="t3://"+server+".mydomain.com.br:7001"
        try:
                connect(adminUserName, 'password0', adminURL)
        except:
                connect(adminUserName, 'password1', adminURL)
                pass

        domainName=domainName
        serverConfig()
        authenticatorPath= '/SecurityConfiguration/' + domainName + '/Realms/' + realmName + '/AuthenticationProviders/DefaultAuthenticator'
        print authenticatorPath
        cd(authenticatorPath)
        print ' '
        print ' '

        print 'Creating Users . . .'
        x=1
        while (x <= int(totalUsers_to_Create)):
                userName = configProps.get("create.user.name."+ str(x))
                userPassword = configProps.get("create.user.password."+ str(x))
                userDescription = configProps.get("create.user.description."+ str(x))
                try:
                        cmo.createUser(userName , userPassword , userDescription)
                        print '-----------User Created With Name : ' , userName
                except:
                        print '*************** Check If the User With the Name : ' , userName ,' already Exists...'
                        x = x + 1
                        print ' '
                        print ' '
                        print 'Adding Group Membership of the Users:'
                y=1
                while (y <= int(totalGroups)):
                        grpName = configProps.get("group.name."+ str(y))
                        groupMembers = configProps.get("group.name."+ str(y) + ".members")
                        usrName=''
                        for usrName in groupMembers.split(','):
                                try:
                                        cmo.addMemberToGroup(grpName,usrName)
                                        print 'USER:' , usrName , 'Added to GROUP: ' , grpName
                                except:
                                        print('Member '+usrName+' can not be found')
                        y=y+1
                        print ' '