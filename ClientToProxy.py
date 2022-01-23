import re
from Mail_format import *
class Receive:
    ClientReplies={}
    # commands = ["EHLO", "AUTH LOGIN", "USER", "PASS", "MAIL FROM", "RCPT TO", "DATA", "QUIT"]
    replies = {"220": "220 127.0.0.1:11111 Local Server.\r\n",
               "250AUTH": "250-Local mail\r\n"
                          "250-PIPELINING\r\n"
                          "250-AUTH LOGIN PLAIN \r\n"
                          "250-AUTH=LOGIN PLAIN\r\n"
                          "250-STARTTLS\r\n"
                          "250 8BITMIME\r\n",
               "221": "221 Bye.\r\n",
               "235": "235 Authentication successful\r\n",
               "250OK": "250 OK\r\n",
               "250END": "250 OK: queued as .\r\n",
               "334USER": "334 VXNlcm5hbWU6\r\n",
               "334PASS": "334 UGFzc3dvcmQ6\r\n",
               "354": "354 End data with<CR><LF>.<CR><LF>.\r\n",
               "500": "500 ERROR\r\n"}

    def __init__(self, con):
        self.conn = con

    def checkmail(self,mail):
        if re.findall('\\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\\b',mail):
            return 1
        else:
            return 0

    def error(self):
        self.conn.send(bytes(self.replies["500"].encode()))
        print("[ProxyToClient]" + self.replies["500"].replace("\r\n", ""))


    def get_message(self):
        message=Mail()

        self.conn.send(bytes(self.replies["220"].encode()))
        print("[ProxyToClient]"+self.replies["220"].replace("\r\n",""))

        m=self.conn.recv(1024).decode()
        if re.search('EHLO', m):
            print("[ClientToProxy]" + m.replace("\r\n", ""))
            message.IDENTITY=m
        else:
            self.error()
            return 0

        self.conn.send(bytes(self.replies["250AUTH"].encode()))
        print("[ProxyToClient]" + self.replies["250AUTH"].rstrip())

        m = self.conn.recv(1024).decode()
        if re.search('AUTH LOGIN', m):
            print("[ClientToProxy]" + m.replace("\r\n", ""))
        else:
            self.error()
            return 0

        self.conn.send(bytes(self.replies["334USER"].encode()))
        print("[ProxyToClient]" + self.replies["334USER"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        message.USER=m
        print("[ClientToProxy]" + m.replace("\r\n", ""))

        self.conn.send(bytes(self.replies["334PASS"].encode()))
        print("[ProxyToClient]" + self.replies["334PASS"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        message.PASS = m
        print("[ClientToProxy]" + m.replace("\r\n", ""))

        self.conn.send(bytes(self.replies["235"].encode()))
        print("[ProxyToClient]" + self.replies["235"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        if re.search('MAIL FROM', m) and self.checkmail(m):
            message.FROM=m
            print("[ClientToProxy]" + m.replace("\r\n", ""))
        else:
            self.error()
            return 0

        self.conn.send(bytes(self.replies["250OK"].encode()))
        print("[ProxyToClient]" + self.replies["250OK"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        while ("RCPT TO" in m) and self.checkmail(m):
            message.TO.append(m)
            print("[ClientToProxy]" + m.replace("\r\n", ""))

            self.conn.send(bytes(self.replies["250OK"].encode()))
            print("[ProxyToClient]" + self.replies["250OK"].replace("\r\n", ""))

            m = self.conn.recv(1024).decode()

        if re.search('DATA', m):
            print("[ClientToProxy]" + m.replace("\r\n", ""))
        else:
            self.error()
            return 0

        self.conn.send(bytes(self.replies["354"].encode()))
        print("[ProxyToClient]" + self.replies["354"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        while "\r\n.\r\n" not in m:
            message.DATA.append(m)
            print("[ClientToProxy]" + m.replace("\r\n", ""))
            m = self.conn.recv(1024).decode()
        print("[ClientToProxy] . ")
        message.DATA.append("\r\n.\r\n")

        self.conn.send(bytes(self.replies["250END"].encode()))
        print("[ProxyToClient]" + self.replies["250END"].replace("\r\n", ""))

        m = self.conn.recv(1024).decode()
        if re.search('QUIT', m):
            print("[ClientToProxy]" + m.replace("\r\n", ""))
        else:
            self.error()
            return 0

        self.conn.send(bytes(self.replies["221"].encode()))
        print("[ProxyToClient]" + self.replies["221"].replace("\r\n", ""))

        self.ClientReplies["IDENTITY"]=message.IDENTITY
        self.ClientReplies["USER"] = message.USER
        self.ClientReplies["PASS"] = message.PASS
        self.ClientReplies["FROM"] = message.FROM
        self.ClientReplies["TO"] = message.TO
        self.ClientReplies["DATA"] = message.DATA

        return self.ClientReplies
