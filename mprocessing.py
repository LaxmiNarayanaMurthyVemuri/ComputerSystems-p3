import os 
import socket
import mimetypes
import subprocess
import multiprocessing

class HTTPServer:
    def __init__(self,host,port):
        socket_1= socket.socket()
        socket_1.bind((host,port))
        socket_1.listen()
        print(f"server is listening on {host}:{port}")
        while True:
            print("Waiting for connection")
            (c,cip) = socket_1.accept()
            print(f'[NEW CONNECTION] {cip} connected.')
            process=multiprocessing.Process(target=self.clientcode, args=(c, ))
            process.start()
            process.join()

    def clientcode(self,c):
        message=c.recv(1000).decode()
        msgsplit=message.splitlines()
        msg=msgsplit[0].split(" ")
        directorypath=msg[1]
        root=os.getcwd()
        filepath=directorypath.split("/")[-1]
        wwwfilenames=os.listdir(os.path.join(root,"www"))
        binfilenames=os.listdir(os.path.join(root,"bin"))
        datapath=root+directorypath
        
        try:
            if directorypath=="/www":
                head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                for file in wwwfilenames:
                    head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                c.sendall(head.encode())

            if directorypath=="/bin":
                head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                for file in binfilenames:
                    head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                c.sendall(head.encode())

            elif os.path.isfile(datapath):
                if filepath in wwwfilenames:
                    f=open(datapath,'rb')
                    result=f.read()
                    f.close()
                    res=f'HTTP/1.1 200 ok \n Content-Type={mimetypes.MimeTypes().guess_type(filepath)[0]}\n Content-Length:{len(str(result))}\n Connection:close\n\n'
                    res=res.encode()
                    res+=result
                    c.sendall(res)

                elif directorypath=="/bin/test.py":
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
                    mess=f'HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:{str(len(f))} \n Connection: close\n\n'
                    res=mess.encode()+f.encode()
                    c.sendall(res)
                
            elif directorypath=="/":
                data="HTTP/1.1 200 OK \n"
                data+="Content-Type: text/html \n"
                data+="Content-Length: " + str(1024) + "\n"
                data+="Connection:close\n"
                data+="\n"
                data+="<html><body><h1>Hehe Webserver under construction</h1></body></html>\n\n"
                c.send(data.encode())

        except:
            mess='HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
            mess+="<html><body><h1>Error 404 File Not found</h1></body></html>\n\n"
            c.send(mess.encode())
        
    
def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
