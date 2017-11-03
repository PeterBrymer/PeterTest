from server.GuiHandler import GuiHandler
from server.SocketHandler import SocketHandler
#calling the methods and giving them inputs from each other
socketHandler = SocketHandler()
guiHandler = GuiHandler(socketHandler)
socketHandler.setGuiHandler(guiHandler)
#starting method getport i guihandler and getting the port from that method.
#sending the port to the sockethandler and then get a result from that.
port = guiHandler.getPort()
resultOfBinding = socketHandler.startToAcceptConnection(port)
#we test if the result of bindning is failed we call on function shoWarningmsg in guihandler
#if not, the function startGui in guiHandler gets started.
if resultOfBinding == "failed":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()

