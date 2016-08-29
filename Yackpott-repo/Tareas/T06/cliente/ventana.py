from datetime import datetime
from PyQt4 import QtGui
import sys

"""
how to use: hay que apretar en el archivo o carpeta
y de ahi el boton a accionar
"""


class Ventana(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.items = dict()
        self.presionado = ""
        self.cliente = None
        self.usuario = ""
        self.otro = ""
        self.setFixedSize(800, 600)
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.rect().center()
        mover = screen - widget
        self.move(mover)

        # archivos
        self.tree = QtGui.QTreeWidget(self)
        self.tree.setMouseTracking(True)
        self.tree.setHeaderHidden(True)
        self.tree.move(25, 50)
        self.tree.resize(200, 480)

        # botones arriba, no necesitan el tree
        self.boton_agregar = QtGui.QPushButton('&Agregar', self)
        self.boton_agregar.move(25, 10)
        self.boton_agregar.resize(102, 32)
        self.boton_agregar.clicked.connect(self.agregar)

        self.boton_actualizar = QtGui.QPushButton('&Actualizar', self)
        self.boton_actualizar.move(125, 10)
        self.boton_actualizar.resize(102, 32)
        self.boton_actualizar.clicked.connect(self.actualizar)

        # botones abajo, necesitan el tree
        self.boton_descargar = QtGui.QPushButton('&Descargar', self)
        self.boton_descargar.move(25, 540)
        self.boton_descargar.resize(102, 32)
        self.boton_descargar.clicked.connect(self.descargar)

        self.boton_historial = QtGui.QPushButton('&Historial', self)
        self.boton_historial.move(125, 540)
        self.boton_historial.resize(102, 32)
        self.boton_historial.clicked.connect(self.historial)

        self.boton_borrar = QtGui.QPushButton('&Borrar', self)
        self.boton_borrar.move(25, 570)
        self.boton_borrar.resize(102, 32)
        self.boton_borrar.clicked.connect(self.borrar)

        self.boton_renombrar = QtGui.QPushButton('&Renombrar', self)
        self.boton_renombrar.move(125, 570)
        self.boton_renombrar.resize(102, 32)
        self.boton_renombrar.clicked.connect(self.renombrar)

        # chat label
        self.label_chat = QtGui.QLabel("Usuario", self)
        self.label_chat.move(345, 20)

        # chat line edit
        self.line_chat = QtGui.QLineEdit("", self)
        self.line_chat.move(400, 15)

        # chat boton chat
        self.boton_chat = QtGui.QPushButton('&Chat!', self)
        self.boton_chat.move(530, 10)
        self.boton_chat.resize(self.boton_chat.sizeHint())
        self.boton_chat.clicked.connect(self.conectar)

        # chat label
        self.chat_conectado = QtGui.QLabel("Chat offline", self)
        self.chat_conectado.move(620, 20)

        # chat box
        self.box_chat = QtGui.QTextEdit("", self)
        self.box_chat.setReadOnly(True)
        self.box_chat.resize(525, 400)
        self.box_chat.move(250, 50)

        # chat text edit
        self.text_chat = QtGui.QTextEdit("", self)
        self.text_chat.resize(525, 90)
        self.text_chat.move(250, 470)

        # chat boton enviar
        self.boton_chat = QtGui.QPushButton('&Enviar', self)
        self.boton_chat.move(650, 560)
        self.boton_chat.resize(self.boton_chat.sizeHint())
        self.boton_chat.clicked.connect(self.enviar_chat)

    @property
    def fecha(self):
        return datetime.now().isoformat(" ").split(".")[0]

    # botones opciones

    def agregar(self):
        self.wid = QtGui.QWidget()
        self.wid.setFixedSize(200, 80)
        self.wid.setWindowTitle("Agregar")
        screen = QtGui.QApplication.desktop().screen().rect().center()
        widget = self.wid.rect().center()
        mover = screen - widget
        self.wid.move(mover)
        boton_archivo = QtGui.QPushButton('&Archivos', self.wid)
        boton_archivo.clicked.connect(self.agregar_archivo)
        boton_archivo.move(10, 25)
        boton_carpeta = QtGui.QPushButton('&Carpetas', self.wid)
        boton_carpeta.clicked.connect(self.agregar_carpeta)
        boton_carpeta.move(100, 25)
        self.wid.show()

    def agregar_archivo(self):
        path = QtGui.QFileDialog.getOpenFileNames()[0]
        self.wid.close()
        self.cliente.agregar(path)
        self.carpetear()

    def agregar_carpeta(self):
        path = QtGui.QFileDialog.getExistingDirectory()
        self.wid.close()
        self.cliente.observar(path)
        self.cliente.actualizar()
        self.carpetear()

    def actualizar(self):
        self.cliente.actualizar()
        self.carpetear()

    def descargar(self):
        path = self.ruta()
        self.cliente.download(path)
        self.carpetear()

    def historial(self):
        path = self.ruta()
        self.cliente.historial(path)
        self.carpetear()

    def borrar(self):
        path = self.ruta()
        self.cliente.eliminar(path)
        self.carpetear()

    # para mover renombrar directorio/archivo.txt
    def renombrar(self):
        path = self.ruta()
        hasta, ok = QtGui.QInputDialog.getText(self, "Renombrar", "Ingresa ruta de destino:")
        if ok:
            self.cliente.renombrar(path, hasta)
            self.carpetear()

    def carpetear(self):
        self.cliente.carpetas()

    """
    como es chico el espacio si con muchas carpetas
    en carpeta lo muestra como por ej progra/nueva
    """
    def carpetas_event(self, event):
        self.items = dict()
        self.tree = QtGui.QTreeWidget(self)
        self.tree.setMouseTracking(True)
        self.tree.setHeaderHidden(True)
        self.tree.move(25, 50)
        self.tree.resize(200, 480)
        dicc = event.dicc
        carpetas = dicc["carpetas"]
        # dicc ruta --> item (no hasheable) :(
        for k, v in carpetas.items():
            if k == "":
                for hijo in v:
                    item = QtGui.QTreeWidgetItem([hijo])
                    self.items[hijo] = item
                    self.tree.addTopLevelItem(item)
            else:
                item = QtGui.QTreeWidgetItem([k])
                self.items[k] = item
                self.tree.addTopLevelItem(item)
                for hijo in v:
                    child = QtGui.QTreeWidgetItem([hijo])
                    self.items[k + "/" + hijo] = child
                    item.addChild(child)
        self.tree.show()

    def ruta(self):
        item = self.tree.currentItem()
        for k, v in self.items.items():
            if v == item:
                self.presionado = k
        print(self.presionado)
        return self.presionado

    def chat(self, evento):
        dicc = evento.dicc
        if "otro" in dicc:
            if dicc["status"] == "ok":
                self.otro = dicc["otro"]
                self.line_chat.setText("")
                self.chat_conectado.setText("Chat: {}".format(self.otro))
                self.chat_conectado.resize(self.chat_conectado.sizeHint())
        if "texto" in dicc:
            texto = dicc["texto"]
            chat = self.box_chat.toPlainText() + "\n" + texto
            self.box_chat.setText(chat)

    def conectar(self):
        texto = self.line_chat.text()
        self.cliente.conectar(self.usuario, texto)

    def enviar_chat(self):
        texto = self.text_chat.toPlainText()
        texto = self.fecha + " " + self.usuario + ": " + texto
        if self.usuario and self.otro and texto:
            self.cliente.chat(self.usuario, self.otro, texto)
            self.text_chat.setText("")
            chat = self.box_chat.toPlainText() + "\n" + texto
            self.box_chat.setText(chat)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
