# imports
import socket
import sys

# main

# def calculation ex: add 900 3212 add 900 and move to port 3212; ex: minus 212 3499, subtract 212 and move on to port 3499
def setup():
    # vars
    port = 3010
    host = sys.argv[1]

    # open socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to web server
    s.connect((host, port))

    # send GET request
    s.sendall("GET / HTTP/1.1\r\n")

    # receive response (receive: operation, number, and port)
    receive = s.recv(4096)
    print(receive)
    pass

def cal(op, num, port):
    pass

if __name__ == "__main__":
    setup()