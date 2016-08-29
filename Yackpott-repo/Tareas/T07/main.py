from PyQt4 import QtGui, QtCore, QtWebKit
import dropbox
import os
import threading
import sys

# pip3 install dropbox

dbx = None
user = None


class Login(QtWebKit.QWebView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(450, 650)
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.rect().center()
        coor = screen - widget
        self.move(coor)

        APP_KEY = "sq6by9pmhwgnoit"
        APP_SECRET = "x5ml2o1vpl1ofk6"

        self.auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        self.authorize_url = self.auth_flow.start()
        self.setUrl(QtCore.QUrl(self.authorize_url))

        self.show()

        self.label_codigo = QtGui.QLabel("Ingrese su token", self)
        self.label_codigo.move(10, 455)
        self.label_codigo.show()

        self.line_codigo = QtGui.QLineEdit("", self)
        self.line_codigo.move(120, 450)
        self.line_codigo.setFixedSize(210, 20)
        self.line_codigo.show()

        self.boton_codigo = QtGui.QPushButton("&TOKEN!", self)
        self.boton_codigo.move(340, 445)
        self.boton_codigo.clicked.connect(self.validar)
        self.boton_codigo.show()

    def validar(self):
        code = self.line_codigo.text()
        access_token, user_id = self.auth_flow.finish(code)
        # variables que nunca cambian, por eso globales
        global dbx
        dbx = dropbox.Dropbox(access_token)
        global user
        user = str(dbx.users_get_current_account().name.display_name)
        self.ventana = Ventana()
        self.close()


# thread encargado de ir actualizando el tree de la ventana principal


class Tree(QtCore.QObject, threading.Thread):
    trigger = QtCore.pyqtSignal()

    def __init__(self, ventana):
        QtCore.QObject.__init__(self)
        threading.Thread.__init__(self)
        self.ventana = ventana
        self.daemon = True
        self.dicc = dict()

    def cargar(self):
        self.rutas()
        self.ventana.items = self.dicc
        self.trigger.connect(self.ventana.cargar_tree)
        self.trigger.emit()

    def rutas(self, path="", padre=None):
        for entry in dbx.files_list_folder(path).entries:
            hijo = QtGui.QTreeWidgetItem([entry.name])
            if (path + "/" + entry.name) not in self.dicc:
                if padre is None:
                    self.ventana.tree.addTopLevelItem(hijo)
                else:
                    padre.addChild(hijo)
                self.dicc[path + "/" + entry.name] = hijo
            if entry.name.count(".") == 0:
                self.rutas(entry.path_lower, hijo)

    # se actualiza cuando se apreta el boton y al inicio
    # se demora eso si
    def run(self):
        self.cargar()


class Ventana(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("#drobpox")
        self.setFixedSize(450, 650)
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.rect().center()
        coor = screen - widget
        self.move(coor)
        self.show()

        self.items = dict()
        self.presionado = None

        self.boton_subir = QtGui.QPushButton('&Subir', self)
        self.boton_subir.move(70, 10)
        self.boton_subir.resize(110, 35)
        self.boton_subir.clicked.connect(self.subir)
        self.boton_subir.show()

        self.boton_descargar = QtGui.QPushButton('&Descargar', self)
        self.boton_descargar.move(170, 10)
        self.boton_descargar.resize(110, 35)
        self.boton_descargar.clicked.connect(self.descargar)
        self.boton_descargar.show()

        self.boton_actualizar = QtGui.QPushButton('&Actualizar', self)
        self.boton_actualizar.move(270, 10)
        self.boton_actualizar.resize(110, 35)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_actualizar.show()

        self.boton_historial = QtGui.QPushButton('&Historial', self)
        self.boton_historial.move(70, 540)
        self.boton_historial.resize(110, 35)
        self.boton_historial.clicked.connect(self.historial)
        self.boton_historial.show()

        self.boton_renombrar = QtGui.QPushButton('&Renombrar', self)
        self.boton_renombrar.move(170, 540)
        self.boton_renombrar.resize(110, 35)
        self.boton_renombrar.clicked.connect(self.renombrar)
        self.boton_renombrar.show()

        self.boton_carpeta = QtGui.QPushButton('&Crear Carpeta', self)
        self.boton_carpeta.move(270, 540)
        self.boton_carpeta.resize(110, 35)
        self.boton_carpeta.clicked.connect(self.carpeta)

        self.label_historial = QtGui.QLabel("", self)
        self.label_historial.setFixedSize(200, 80)
        self.label_historial.move(25, 560)
        self.label_historial.show()

        self.boton_carpeta.show()

        self.llamar_tree()

    # inicia el thread del tree
    def llamar_tree(self):
        self.tree = QtGui.QTreeWidget(self)
        obj = Tree(self)
        obj.start()

    # recibe el trigger
    def cargar_tree(self):
        self.tree.setHeaderHidden(True)
        self.tree.move(25, 50)
        self.tree.resize(400, 480)
        self.tree.show()

    # parte el thread de subir
    def subir(self):
        ruta = QtGui.QFileDialog.getOpenFileNames()[0]
        archivo = ruta.split("/")[-1]
        t1 = threading.Thread(target=self.thread_subir, args=(ruta, archivo))
        t1.daemon = True
        t1.start()

    # thread que habla con dropbox para subir archivo
    def thread_subir(self, ruta, relativa):
        with open(ruta, "rb") as file:
            dbx.files_upload(file, "/" + relativa)

    # saca la ruta inicial
    def descargar(self):
        path = self.ruta()
        self.buscar_descargar(path)

    # saca todos los archivos recusirvamente
    def buscar_descargar(self, path):
        if path.count(".") == 0:
            for entry in dbx.files_list_folder(path).entries:
                self.buscar_descargar(path + "/" + entry.name)
        else:
            t1 = threading.Thread(target=self.thread_descargar, args=(path,))
            t1.daemon = True
            t1.start()

    # thread que baja los archivos de dropbox
    def thread_descargar(self, path):
        md, res = dbx.files_download(path)
        data = res.content
        path = user + "/" + path
        carpeta = "/".join(path.split("/")[:-1])
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        with open(path, "wb+") as file:
            file.write(data)

    # actualiza el tree, se demora harto igual
    def actualizar(self):
        self.llamar_tree()

    # obtiene el metada y lo pone en el label
    def historial(self):
        path = self.ruta()
        info = dbx.files_get_metadata(path)
        texto = "Historial:\nName: {}\nPath: {}\n{}".format(
            info.name, info.path_lower, info.id)
        self.label_historial.setText(texto)

    # formato ej Conta 2/Mates Discretas.pdf
    # tambien funciona con carpetas
    def renombrar(self):
        path = self.ruta()
        if path:
            self.wid = QtGui.QWidget()
            self.wid.setFixedSize(200, 80)
            self.wid.setWindowTitle("Renombrar")
            self.wid_line = QtGui.QLineEdit("", self.wid)
            self.wid_line.setFixedSize(180, 20)
            self.wid_line.move(10, 15)
            self.wid_boton = QtGui.QPushButton("&Renombrar", self.wid)
            self.wid_boton.move(50, 40)
            self.wid_boton.clicked.connect(self.click_renombrar)
            screen = QtGui.QApplication.desktop().screen().rect().center()
            widget = self.wid.rect().center()
            coor = screen - widget
            self.wid.move(coor)
            self.wid.show()

    # recibe la direccion de destino
    def click_renombrar(self):
        path = self.ruta()
        nueva = "/" + self.wid_line.text()
        self.wid.close()
        t1 = threading.Thread(target=self.thread_renombrar, args=(path, nueva))
        t1.daemon = True
        t1.start()

    # thread para que no se lagee
    def thread_renombrar(self, path, nueva):
        dbx.files_move(path, nueva)

    # crea un carpeta en el directorio seleccionado de la forma
    # Nombre_Carpeta
    def carpeta(self):
        self.wid = QtGui.QWidget()
        self.wid.setFixedSize(200, 80)
        self.wid.setWindowTitle("Crear Carpeta")
        self.wid_line = QtGui.QLineEdit("", self.wid)
        self.wid_line.setFixedSize(180, 20)
        self.wid_line.move(10, 15)
        self.wid_boton = QtGui.QPushButton("&Crear", self.wid)
        self.wid_boton.move(65, 40)
        self.wid_boton.clicked.connect(self.click_carpeta)
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.wid.rect().center()
        coor = screen - widget
        self.wid.move(coor)
        self.wid.show()

    # recibe la segunda parte del path
    def click_carpeta(self):
        path = self.ruta()
        if not path:
            path = ""
        otra = self.wid_line.text()
        final = path + "/" + otra
        t1 = threading.Thread(target=self.thread_carpeta, args=(final,))
        t1.daemon = True
        t1.start()
        self.wid.close()

    # se hace con thread para que no se quede pegado
    def thread_carpeta(self, path):
        dbx.files_create_folder(path)

    def ruta(self):
        item = self.tree.currentItem()
        for k, v in self.items.items():
            if v == item:
                self.presionado = k
        return self.presionado

    def closeEvent(self, QCloseEvent):
        try:
            self.wid.close()
        except:
            pass
        QCloseEvent.accept()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec_())
