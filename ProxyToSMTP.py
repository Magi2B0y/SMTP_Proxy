import re
import socket
import smtplib

class Send:
    def __init__(self,SMTP_host,SMTP_port):
        self.conn = socket.socket()
        self.conn.connect((SMTP_host,SMTP_port))

    def error(self):
        print("ERROR! Please Resend")

    def SendToSMTP(self,message):
        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]"+m.replace("\r\n", ""))

        if "220" in m:
            self.conn.send(bytes(message["IDENTITY"].encode()))
            print("[ProxyToSMTP]" + message["IDENTITY"].replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "250" in m:
            self.conn.send(bytes("AUTH LOGIN\r\n".encode()))
            print("[ProxyToSMTP]" + "AUTH LOGIN")
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "334" in m:
            self.conn.send(bytes(message["USER"].encode()))
            print("[ProxyToSMTP]" + message["USER"].replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "334" in m:
            self.conn.send(bytes(message["PASS"].encode()))
            print("[ProxyToSMTP]" + message["PASS"].replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "235" in m:
            self.conn.send(bytes(message["FROM"].encode()))
            print("[ProxyToSMTP]" + message["FROM"].replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        for email_to in  message["TO"]:
            if "250" in m:
                self.conn.send(bytes(email_to.encode()))
                print("[ProxyToSMTP]" + email_to.replace("\r\n", ""))

                m = self.conn.recv(1024).decode()
                print("[SMTPToProxy]" + m.replace("\r\n", ""))
            else:
                self.error()
                return 0

        if "250" in m:
            self.conn.send(bytes("DATA\r\n".encode()))
            print("[ProxyToSMTP]" + "DATA".replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "354" in m:
            for data in message["DATA"]:
                self.conn.send(bytes(data.encode()))
                print("[ProxyToSMTP]" + data.replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "250" in m:
            self.conn.send(bytes("QUIT\r\n".encode()))
            print("[ProxyToSMTP]" + "QUIT".replace("\r\n", ""))
        else:
            self.error()
            return 0

        m = self.conn.recv(1024).decode()
        print("[SMTPToProxy]" + m.replace("\r\n", ""))

        if "221" in m:
            print("\r\nCompleted\r\n")
        else:
            self.error()
            return 0
        self.conn.close()
        return 1

