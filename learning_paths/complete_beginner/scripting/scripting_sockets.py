# imports
import socket
import sys
import time
import re

# main
def main():
    # set initial vars
    port = 1337
    old_num = 0
    server = sys.argv[1]

    # LOOP: until recv = STOP or port=9765
    while port != 9756:
        try: 
            # socket operation (open & connect)
            s = socket.socket()
            s.connect((server, port))

            # send GET request
            request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" %server
            s.send(request.encode("utf8"))

            # recevie response
            resp = s.recv(4096)

            # parse data recevived
            data = resp.decode("utf8")
            parsed_data = re.split(' |\*|\n', data)
            parsed_data = list(filter(None, parsed_data))
            
            # print(data)
            # print(parsed_data)       

            # assign/update vars
            old_port = port
            port = int(parsed_data[-1])
            op = float(parsed_data[-3])
            new_num = float(parsed_data[-2])

            # do calculation based on response
            print("calculating")
            if (port != old_port):
                old_num = calc(op, num)
            print(old_num)

            # close connection
            s.close()

        # ports update every 4 seconds
        except:
            s.close()
            time.sleep(3)
            print("Sleeping")
            pass

def calc(op, old_num, new_num):
    if op == "add":
        return old_num + new_num
    elif op == "minus":
        return old_num - new_num
    elif op == "multiply":
        return old_num * new_num
    elif op == "divide":
        return old_num / new_num
    else:
        return None

if __name__ == "__main__":
    main()