from PyQt4 import QtGui, uic
from calc_financiero import calcular_jub

form = uic.loadUiType("hexa.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pix_1 = QtGui.QPixmap("logo_argentum.png")
        pix_3 = QtGui.QPixmap("logo_hexa.png")
        self.label_1.setPixmap(pix_1)
        self.label_3.setPixmap(pix_3)
        self.lineEdit_1.textChanged.connect(self.calcular)
        self.lineEdit_2.textChanged.connect(self.calcular)
        self.lineEdit_3.textChanged.connect(self.calcular)
        self.lineEdit_4.textChanged.connect(self.calcular)
        self.lineEdit_5.textChanged.connect(self.calcular)
        self.comboBox.currentIndexChanged.connect(self.calcular)
        # Completar la creación de la interfaz #

    def calcular(self):
        seguir = True
        if self.lineEdit_1 == "":
            seguir = False
        elif self.lineEdit_2 == "":
            seguir = False
        elif self.lineEdit_3 == "":
            seguir = False
        elif self.lineEdit_4 == "":
            seguir = False
        elif self.lineEdit_5 == "":
            seguir = False
        elif self.comboBox == "":
            seguir = False

        if seguir:
            try:
                self.aporte = int(self.lineEdit_1.text())*int(self.lineEdit_2.text())/100
                self.label_aporte.setText(str(self.aporte))
                self.anos = float(self.lineEdit_5.text())-float(self.lineEdit_4.text())
                self.label_pension.setText(str(self.anos))
                self.ingreso = float(self.lineEdit_1.text())
                self.cotiza = float(self.lineEdit_2.text())
                self.edad = float(self.lineEdit_3.text())
                self.edad_j = float(self.lineEdit_4.text())
                self.esp_vida = float(self.lineEdit_5.text())
                self.fondo_elegido = self.comboBox.itemText(self.comboBox.currentIndex())
                rango = calcular_jub(self.ingreso,self.cotiza, self.edad, self.edad_j, self.esp_vida, self.fondo_elegido)
                self.label_rango.setText(rango)
                print("termino")
            except Exception as err:
                print(err)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
