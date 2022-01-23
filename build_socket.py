import socket
from ClientToProxy import *
from ProxyToSMTP import *
import threading
def listen(host,port):
    tcp_socket=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    tcp_socket.listen()
    print("Start Listening  "+host+":"+str(port))
    while True:
        conn, (host,port) = tcp_socket.accept()
        print("\r\n===============ClientToProxy===============")
        receive=Receive(conn)
        message = receive.get_message()
        conn.close()
        # print(message)
        if message:
            SMTP_host,SMTP_port= "smtp.qq.com",25
            send=Send(SMTP_host,SMTP_port)
            print("\r\n===============ProxyToSMTP===============")
            send_thread = threading.Thread(target=send.SendToSMTP,args=(message,),daemon = True)
            send_thread.start()
            # send_thread.close()
        else:
            print("Please Resend")
            continue