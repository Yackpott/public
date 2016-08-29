from PyQt4 import QtGui
import sys


class Login(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.cliente = None
        self.ventana = None
        self.err = "Bad User/Pass"
        self.setFixedSize(300, 300)
        self.setWindowTitle("Drobpox")
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.rect().center()
        mover = screen - widget
        self.move(mover)

        # user label
        self.label_user = QtGui.QLabel("Usuario", self)
        self.label_user.move(50, 80)

        # pass label
        self.label_pass = QtGui.QLabel("Password", self)
        self.label_pass.move(50, 110)

        # user line edit
        self.line_user = QtGui.QLineEdit("", self)
        self.line_user.move(120, 80)

        # pass line edit
        self.line_pass = QtGui.QLineEdit("", self)
        self.line_pass.setEchoMode(QtGui.QLineEdit.Password)
        self.line_pass.move(120, 110)

        # login boton
        self.boton_login = QtGui.QPushButton('&Login', self)
        self.boton_login.move(75, 140)
        self.boton_login.resize(self.boton_login.sizeHint())
        self.boton_login.clicked.connect(self.logear)

        # nuevo boton
        self.boton_nuevo = QtGui.QPushButton('&Nuevo', self)
        self.boton_nuevo.move(155, 140)
        self.boton_nuevo.resize(self.boton_nuevo.sizeHint())
        self.boton_nuevo.clicked.connect(self.nuevear)

        # status label
        self.label_status = QtGui.QLabel("", self)
        self.label_status.move(110, 190)
        self.show()

    def logear(self):
        self.usuario = self.line_user.text()
        self.password = self.line_pass.text()
        self.cliente.login(self.usuario, self.password)

    def nuevear(self):
        usuario = self.line_user.text()
        password = self.line_pass.text()
        self.cliente.nuevo(usuario, password)

    def login_event(self, event):
        dicc = event.dicc
        if dicc["tipo"] == "login":
            if dicc["status"] == "ok":
                self.close()
                self.ventana.usuario = self.usuario
                self.ventana.setWindowTitle(self.usuario)
                self.ventana.carpetear()
                self.ventana.show()
            else:
                self.label_status.setText("Bad user/pass")
        if dicc["tipo"] == "nuevo":
            if dicc["status"] == "ok":
                self.label_status.setText("Usuario creado!")
            else:
                self.label_status.setText("Already exists")
        self.label_status.resize(self.label_status.sizeHint())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
