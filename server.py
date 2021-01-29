#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #get the data and split the data received by spaces
        self.data = self.request.recv(1024).strip()
        msg = self.data.decode("utf-8").split(' ')

        #check if the request is a get method
        if (msg[0] == 'GET'):

            #check the path and display the correct html webpage with styling added based off the path
            if (msg[1] == '/deep/' or msg[1] == '/hardcode/deep/' or msg[1] == '/hardcode/'):
                html_file = open('./www' + msg[1] + 'index.html', 'r')
                css = open('./www' + msg[1] + 'deep.css', 'r')
                self.request.sendall(str.encode("HTTP/1.1 200 OK\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode(html_file.read(), 'utf-8'))
                self.request.sendall(str.encode("<style>\n", 'utf-8'))
                self.request.sendall(str.encode(css.read(), 'utf-8'))
                self.request.sendall(str.encode("</style>\n", 'utf-8'))
            elif(msg[1] == '/' or msg[1] == '/index.html'): 
                html_file = open('./www/index.html', 'r')
                css = open('./www/base.css', 'r')
                self.request.sendall(str.encode("HTTP/1.1 200 OK\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode(html_file.read(), 'utf-8'))
                self.request.sendall(str.encode("<style>\n", 'utf-8'))
                self.request.sendall(str.encode(css.read(), 'utf-8'))
                self.request.sendall(str.encode("</style>\n", 'utf-8'))
            elif(msg[1] == '/deep/index.html' or msg[1] == '/hardcode/index.html' or msg[1] == '/hardcode/deep/index.html'):
                html_file = open('./www' + msg[1], 'r')
                css = open('./www' + msg[1][:len(msg[1])-10] + 'deep.css', 'r')
                self.request.sendall(str.encode("HTTP/1.1 200 OK\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode(html_file.read(), 'utf-8'))
                self.request.sendall(str.encode("<style>\n", 'utf-8'))
                self.request.sendall(str.encode(css.read(), 'utf-8'))
                self.request.sendall(str.encode("</style>\n", 'utf-8'))
            
            #return the specified css file
            elif(msg[1] == '/base.css' or msg[1] == '/deep/deep.css' or msg[1] == '/hardcode/deep.css' or msg[1] == '/hardcode/deep/deep.css'):
                css = open('./www' + msg[1], 'r')
                self.request.sendall(str.encode("HTTP/1.1 200 OK\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/css\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode(css.read(), 'utf-8'))

            #check for 301 errors with missing slashes
            elif(msg[1] == '/deep' or msg[1] == '/hardcode' or msg[1] == '/hardcode/deep'):
                self.request.sendall(str.encode("HTTP/1.1 301 Moved Permanently\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode('<html><head></head><body><h1>301 Moved Permanently</h1><p>Location: http://localhost:8080' + msg[1] + '/</p></body></html>', 'utf-8'))
            
            #display 404 if webpage requested is not found
            else:
                self.request.sendall(str.encode("HTTP/1.1 404 Not Found\n", 'utf-8'))
                self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
                self.request.send(str.encode('\r\n'))
                self.request.sendall(str.encode('<html><head></head><body><h1>404 Not Found</h1></body></html>', 'utf-8'))
        
        #display 405 if the method is anything but a get request.
        else:
            self.request.sendall(str.encode("HTTP/1.1 405 Method Not Allowed\n", 'utf-8'))
            self.request.sendall(str.encode("Content-Type: text/html\n", 'utf-8'))
            self.request.send(str.encode('\r\n'))
            self.request.sendall(str.encode('<html><head></head><body><h1>405 Method Not Allowed</h1></body></html>', 'utf-8'))

        #close the socket request
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
