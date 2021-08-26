from socket import *
server="127.0.0.1"
port=2121
connection = socket(AF_INET,SOCK_STREAM)
connection.connect((server,port))

while True:
    command=input("Enter Your Command: ")
    splittedCommand=command.lower().split(' ')
    if splittedCommand[0]=="help":
        print("LIST | For See Directory files and folders information")
        print("DWLD filepath | For Download file from server")
        print("PWD | For see current Directory")
        print("CD dirName | For Open Folder dirName")
        print("HELP | For Commands Help")
    elif splittedCommand[0]=="pwd":
        connection.send("pwd".encode())
        dir=connection.recv(1024)
        print("Currnet Directory is :"+dir.decode())
    elif splittedCommand[0]=="list":
        connection.send("list".encode())
        dir=connection.recv(1024).decode()
        print("List of Files :\n"+dir)
    elif splittedCommand[0]=="cd":
        connection.send(("cd "+splittedCommand[1]).encode())
        result=connection.recv(1024)
        print("Result : "+result.decode())
    elif splittedCommand[0]=="dwld" :
        connection.send(("dwld "+splittedCommand[1]).encode())
        result=connection.recv(1048576).decode().split(" ")
        if result[0]=="true":
            print("Download Port is : "+result[1])
            DataChannel=socket(AF_INET,SOCK_STREAM)
            DataChannel.connect((server,int(result[1])))
            f=open(splittedCommand[1],"wb")
            for x in range(int(int(result[2])/1024)+1):
                data=DataChannel.recv(1024)
                f.write(data)
            f.close()
            print("File Downloaded Successfully!")
            connection.send("Finish".encode())
            DataChannel.close()
        else:
            print("Bad Request!")
    elif splittedCommand[0]=="quit":
        connection.send("quit".encode())
        connection.close()
        exit()
    else:
        print("Command is Invalid !")



