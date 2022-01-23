import threading
import  sys
import  time
from build_socket import *
host = '127.0.0.1'
port = 11111

def main():
    build_socket_thread = threading.Thread(target=listen, args=(host, port), daemon=True)
    build_socket_thread.start()
    while True:
        try:
            time.sleep(100)
        except KeyboardInterrupt:
            print("END!")
            sys.exit()

if __name__ == "__main__":
    main()