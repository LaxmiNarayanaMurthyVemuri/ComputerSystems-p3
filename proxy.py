'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

'''
from http import server
import os 
import socket
import mimetypes
import subprocess

class HTTPServer:
    def __init__(self,host,port):
        socket_1= socket.socket()
        socket_1.bind((host,port))
        socket_1.listen()
        print(f"server is listening on {host}:{port}")
        while True:
            print("Waiting for connection")
            (c,cip) = socket_1.accept()
            message=c.recv(1000).decode()
            # print(message)
            msgsplit=message.splitlines()
            # print(msgsplit[0])
            msg=msgsplit[0].split(" ")
            # print(msg)
            directorypath=msg[1]
            # print("this is directory path+++++++++++++++++++=",directorypath)
            root=os.getcwd()
            # print("+===============+",root)
            filepath=directorypath.split("/")[-1]
            # print("this is filepath==================================", filepath)
            filenames=os.listdir(os.path.join(root,"www"))

            filename3=os.listdir(os.path.join(root,"bin"))
            # print(filename3)

            datapath=root+directorypath
            # print(datapath)
            # print(os.path.join(root,"www"))
            # print(filenames)
            try:
                if directorypath=="/www":
                    head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                    for file in filenames:
                        head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                    c.sendall(head.encode())

                if directorypath=="/bin":
                    head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                    for file in filename3:
                        head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                    c.sendall(head.encode())

                elif os.path.isfile(datapath):
                    if filepath in filenames:
                        f=open(datapath,'rb')
                        result=f.read()
                        f.close()
                        res=f'HTTP/1.1 200 ok \n Content-Type={mimetypes.MimeTypes().guess_type(filepath)[0]}\n Content-Length:{len(str(result))}\n Connection:close\n\n'
                        res=res.encode()
                        res+=result
                        c.sendall(res)

                    elif directorypath=="/bin/test.py":
                        # print(True)
                        process=subprocess.Popen(['python','C:\\Users\\Swapneeth Punna\\Desktop\\DS\\CS\\ComputerSystems-p1\\ComputerSystem-p3\\ComputerSystems-p3\\bin\\test.py'], shell=False, stdout=subprocess.PIPE) 
                        comm = process.communicate()[0] 
                        d=comm.decode()
                        mess='HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
                        me=mess.encode()
                        de=d.encode()
                        res=me+de
                        c.sendall(res)

                    elif directorypath=="/bin/ls":
                        p=os.popen('dir')
                        f=p.read()
                        mess='HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
                        res=mess.encode()+f.encode()
                        c.sendall(res)
                    
                    # elif directorypath=="/bin/du":
                    #     p=os.popen('diskusage/?')
                    #     # print(p)
                    #     f=p.read()
                    #     messag='HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
                    #     result=messag.encode()+f.encode()
                    #     c.sendall(result)
                        
                    # elif directorypath=="/bin/ls":
                    #     res=subprocess.run('dir',shell=True,stdout=True)
                    #     res=str(res)
                    #     mess='HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
                    #     result=mess.encode()+res.encode()
                    #     c.sendall(result)

                elif directorypath=="/":
                    data="HTTP/1.1 200 OK \n"
                    data+="Content-Type: text/html \n"
                    data+="Content-Length: " + str(1024) + "\n"
                    data+="Connection:close\n"
                    data+="\n"
                    data+="<html><body><h1>Hehe Webserver under construction</h1></body></html>\n\n"
                    c.send(data.encode())

            except:
                c.send("HTTP/1.1 404 not found".encode())
            # print(False)
                socket_1.close()


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
