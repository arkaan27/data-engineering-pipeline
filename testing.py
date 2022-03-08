import socket
from requests import get
if __name__ == "__main__":

    ip = get('https://api.ipify.org').content.decode('utf8')
    print('My public IP address is: {}'.format(ip))

    hostname= ip + ":27017"
    print(hostname)