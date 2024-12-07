import socket
import threading
import socketserver
import sys                                                                  
import signal
 
def quit(signum, frame):
    sys.exit()


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    '''处理客户端请求对应的类'''
    def handle(self):
        '''收到请求后执行的处理函数'''
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)
 
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''用来创建服务器的类，也可以不用定义直接调用'''
    pass
 
def client(ip, port, message):
    '''模拟客户端收发消息'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
 
if __name__ == "__main__":
    '''端口写零自动使用系统可用端口'''
    HOST, PORT = "127.0.0.1", 9001
    '''创建服务器，采用线程模式，前一个请求未处理完也可以接收下一个请求'''
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    '''在请求处理类里自定义的方法在服务器端不可以调用'''
    with server:
        ip, port = server.server_address
 
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
 
        # client(ip, port, "Hello World 1")
        # client(ip, port, "Hello World 2")
        # client(ip, port, "Hello World 3")
 
        # server.shutdown()
    while True:
        try:
            signal.signal(signal.SIGINT, quit)
            signal.signal(signal.SIGTERM, quit)

        except:
            break
    print("shutdown")
    server.shutdown()