tasks = []
for server in cmo.getServerLifeCycleRuntimes():
    # to shut down all servers
    if (server.getName() != ‘AdminServer’ and server.getState() != ‘RUNNING’ ):
        tasks.append(server.start())
    #or to start them up:
    #if (server.getName() != ‘AdminServer’ and server.getState() != ‘SHUTDOWN’ ):
    #   tasks.append(server.shutdown())


#wait for tasks to complete
while len(tasks) > 0:
    for task in tasks:
        if task.getStatus()  != ‘TASK IN PROGRESS’ :
            tasks.remove(task)

    java.lang.Thread.sleep(5000)