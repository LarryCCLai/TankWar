from WorkWidgets.MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip
import sys


from client.SocketClient import SocketClient



host = "140.113.150.236"
port = 20001
BUFFER_SIZE = 1940
client = SocketClient(host, port)

app = QApplication([])
main_window = MainWidget(client)
main_window.setFixedSize(1080, 864)
main_window.show()

# main_window.showFullScreen()

sys.exit(app.exec_())