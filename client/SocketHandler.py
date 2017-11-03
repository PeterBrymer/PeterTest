import socket
import _thread
#class that handles the socket related stuffs
class SocketHandler:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #setting the guihandler that gets inputed in main to self.guihandler so we can use it in this class
    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_
    #the connect method that try if we can connect to the server with the entred ip and port.
    #if not we get no connection
    def connect(self,ip, port):
        try:
            self.clientSocket.connect((ip,int(port)))
            self.startReceiverThread()
        except:
            return "no connection"
    #the method send message to the server from de client, if not pass
    def sendMsg(self,text):
        try:
            self.clientSocket.send(str.encode(text))
        except:
            pass
    #starting the thread that handle the receive and the function the thread will use is startreceiving
    def startReceiverThread(self):
        _thread.start_new_thread(self.startReceiving,())
    #the method that receiving things from the server, and then sendint the message to the gui so the gui can print it
    # if the user disconnect the receiver is the thing that will call this to the guihandler and show the message on gui
    def startReceiving(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode()
                self.guiHandler.showMessage(msg)
            except:
                self.guiHandler.showMessage("desconnected...")
                return