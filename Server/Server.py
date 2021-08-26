import os , random
from socket import *

server = "127.0.0.1"
port = 2121
directory = "files"
socket1 = socket(AF_INET,SOCK_STREAM)
socket1.bind((server,port))
socket1.listen(10)
print("Listening on 127.0.0.1 and Port : 2121 ...\n")
os.chdir(directory)
fullDir=os.getcwd()
connection,address = socket1.accept()
print("Client Connected by {} IP Address on Port 2121".format(address))

def getDir():
    if os.getcwd().endswith("files"):
        return "\\"
    else:
        return "\\"+os.getcwd().removeprefix(fullDir)
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


while True:
    command = connection.recv(1024).decode()
    splittedCommand = command.lower().split(" ")

    if splittedCommand[0] == "pwd":
       connection.send(getDir().encode())
       print("Returned Current Directory")

    elif splittedCommand[0] == "list":
       print("Generating List of Directory...")
       ListResult = ""
       size = 0
       for x in os.listdir():
           if os.path.isdir(x):
               size+=getFolderSize(x)
               ListResult+="<   {0} - {1}\n".format(x,getFolderSize(x))
           else:
               size+=os.path.getsize(x)
               ListResult+="    {0} - {1}\n".format(x,os.path.getsize(x))
       ListResult+="Total size : {0}".format(size)
       connection.send(ListResult.encode())
       print("List of Directory sent success !")

    elif splittedCommand[0] == "cd":
       if splittedCommand[1]=="..":
           currentDir=os.getcwd()
           os.chdir(splittedCommand[1])
           if os.getcwd().startswith(fullDir):
               print("Directory has Changed ! \n new Directory : {}".format(getDir()))
               connection.send("Directory Changed successfully ! \n Now You are in {}".format(getDir()).encode())
           else:
               os.chdir(currentDir)
               print("Access Denied!")
               connection.send("Access Denied!".encode())

       elif os.path.exists(splittedCommand[1]):
           currentDir=os.getcwd()
           os.chdir(splittedCommand[1])
           if os.getcwd().startswith(fullDir):
               print("Directory has Changed ! \n new Directory : {}".format(getDir()))
               connection.send("Directory Changed successfully ! \n Now You are in {}".format(getDir()).encode())
           else:
               os.chdir(currentDir)
               print("Access Denied!")
               connection.send("Access Denied!".encode())
       else:
            print("Bad Requst")
            connection.send("Directory does not Exist!".encode())

    elif splittedCommand[0] == "dwld" :
       fileName=splittedCommand[1]
       if os.path.exists(fileName):
           tempPort = random.randint(3000, 50000)
           connection.send(("true "+str(tempPort)+" "+str(os.path.getsize(splittedCommand[1]))).encode())
           data = socket(AF_INET, SOCK_STREAM)
           data.bind((server, tempPort))
           data.listen()
           connection1,address = data.accept()
           f=open(fileName,"rb")
           connection1.send(f.read())
           if connection.recv(1024).decode()=="Finish":
               data.close()
           print("File Sent Successfully!\n")
       else:
           connection.send("File Not Found!".encode())
           print("File Not Found!\n")
    elif splittedCommand[0]=="quit":
        socket1.close()
        exit()
    else:
        print("Command is Invalid !")
   
