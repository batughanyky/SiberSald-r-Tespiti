import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from log_ui import Ui_LogWindow
from packet_classifier import PacketClassifier

class LogWindow(QMainWindow, Ui_LogWindow):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.setupUi(self)
        self.packet_classifier = PacketClassifier(self)

    def update_status(self, status):
        self.status_label.setText(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LogWindow()
    window.show()
    sys.exit(app.exec_())
