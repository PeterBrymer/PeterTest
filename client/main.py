from client.GuiHandler import GuiHandler
from client.SocketHandler import SocketHandler
#calling methods from gui and socket handler so they get active
socketHandler = SocketHandler()
guiHandler = GuiHandler(socketHandler)
socketHandler.setGuiHandler(guiHandler)
#getting the port and ip from the gui window
ip,port = guiHandler.getIpAndPort()
#conneting to server with the ip and port in the socket handler
resultOfConnection = socketHandler.connect(ip,port)
#if the answer we get from the socket is no connection we get a warning, if not the gui start up
if resultOfConnection == "no connection":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()