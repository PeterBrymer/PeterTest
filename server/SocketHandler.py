import socket
import _thread
import sys
from server.Users import CollectionOfUsers
#a class that handle the sockets and threads
class SocketHandler:
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.users = CollectionOfUsers()
        self.users.readUsersFromFile()
    #declare guihandle as a self variable, the main method calls on this method
    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_
    #a method that close the socket and call on the users method write to file. Then exit the program.
    #getting trigged from the guihandler
    def closeEveryThing(self):
        self.serverSocket.close()
        self.users.writeUsersToFile()
        sys.exit(0)
    #a method that wait for connection from a client and give the client a clientsocket and client addres
    #put the client socket in a list of unknown clients and addr, then start the reciverThread.
    #if that not work we pass.
    def startAccepting(self):
        while True:
            try:
                clientSocket, clientAddr = self.serverSocket.accept()
                self.list_of_unknown_clientSockets.append(clientSocket)
                self.list_of_unknown_clientAddr.append(clientAddr)
                self.startReceiverThread(clientSocket, clientAddr)

            except:
                pass
    #the method that the main method call on.
    #the method trying to bind a socket with the ip from main method, if it not works it return failed.
    #then the serversocket start listen for connection.
    #creating the list of known and unknown clientsockets and clientaddr.
    #starting thread and trigger the method startAccepting and then return succeed
    def startToAcceptConnection(self,port):
        try:
            self.serverSocket.bind(('',int(port)))
        except:
            return "failed"
        self.serverSocket.listen()

        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []

        _thread.start_new_thread(self.startAccepting,())
        return "succeed"
    #method that sends the message to all the client in the known list and show it on the gui for the server
    def sendAndShowMsg(self, text):
        self.guiHandler.showMessage(text)
        for clientSock in self.list_of_known_clientSockets:
            clientSock.send(str.encode(text))
    #method that starts the reciving thread and put in the clientsocket and client addr in to the startreciving method
    def startReceiverThread(self, clientSocket, clientAddr):
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))
    #a method that removes the client from the unknownd list and append the client to the knownd list if the result of
    #listentounknownclient is not equal to false. Also trigger the method listentoknownclient and send the cleintsocket and username
    def startReceiving(self,clientSocket, clientAddr):
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin
            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)

            self.list_of_known_clientSockets.append(clientSocket)
            self.list_of_known_clientAddr.append(clientAddr)

            self.listenToknownClinet(clientSocket,clientAddr,username)
    #a method that listen if the unknown client trying to login or create a user through the message field.
    #if the user exist the user gets logined in if not the user get the not ok message from the server
    #if the user wanna register the user needs to put in username, password, email and name with space between
    # if it works the user gets created. Otherwise the user gets message from server, not fine.
    def listenToUnknownClinet(self,clientSocket, clientAddr):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
            except:
                self.list_of_unknown_clientSockets.remove(clientSocket)
                self.list_of_unknown_clientAddr.remove(clientAddr)
                return False

            args = msg.split(' ')
            if len(args) == 3 and args[0] == "login":
                username = args[1]
                password = args[2]
                if self.users.doesThisUserExistAndNotActive(username,password):
                    clientSocket.send(str.encode("ok"))
                    self.sendAndShowMsg(username + " is connected")
                    return username
                else:
                    clientSocket.send(str.encode("not ok"))

            if len(args) >= 5 and args[0] == "register":
                username = args[1]
                password = args[2]
                email = args[3]
                name = ""
                for rest in args[4:]:
                    name += rest + " "
                if username != "" and password != "" and email != "" and name != "":
                    resultOfAdding = self.users.add_user(username,password,email,name)
                    if resultOfAdding == True:
                        clientSocket.send(str.encode("fine"))
                    else:
                        clientSocket.send(str.encode("not fine"))
                else:
                    clientSocket.send(str.encode("not fine"))
    #the method that listen to clients and broadcast the message to all users.
    #if the user disconnect the client socket get removed from the known clients and the user get put as an inactiveUser
    def listenToknownClinet(self,clientSocket, clientAddr,username):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
                self.sendAndShowMsg(username + ": " + msg)
            except:
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg(username+" disconnected")
                self.users.inactiveUser(username)
                return
