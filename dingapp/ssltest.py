__author__ = 'rwang'

import httplib
import socket
import ssl
import urllib2

def connect(self):
    "Connect to a host on a given (SSL) port."

    sock = socket.create_connection((self.host, self.port),
                                    self.timeout, self.source_address)
    if self._tunnel_host:
        self.sock = sock
        self._tunnel()

    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)

httplib.HTTPSConnection.connect = connect

opener = urllib2.build_opener()
f = opener.open('https://oapi.dingtalk.com/user/list?access_token=b5c150ac36543a7facec865b16d6b46a&department_id=1')
print f.read()

