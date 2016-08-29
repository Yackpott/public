import unittest
from os import listdir
from main import Corrector


class Test(unittest.TestCase):

    def setUp(self):
        r1 = open("5435466-5_lucas_hidalgo.txt", "r")
        r2 = open("6968271-5_Andrea_valdes.ttxtt", "r")
        r3 = open("18936676-0_antonio_lopez.txt", "r")
        r4 = open("18936677-k_rodrigo_lave.txt", "r")
        self.r1 = r1.readlines()
        self.r2 = r2.readlines()
        self.r3 = r3.readlines()
        self.r4 = r4.readlines()
        r1.close()
        r2.close()
        r3.close()
        r4.close()
        self.corr1 = Corrector("5435466-5_lucas_hidalgo.txt")
        self.corr2 = Corrector("6968271-5_Andrea_valdes.ttxtt")
        self.corr3 = Corrector("18936676-0_antonio_lopez.txt")
        self.corr4 = Corrector("18936677-k_rodrigo_lave.txt")


    def tearDown(self):
        r1 = open("5435466-5_lucas_hidalgo.txt", "w")
        r2 = open("6968271-5_Andrea_valdes.ttxtt", "w")
        r3 = open("18936676-0_antonio_lopez.txt", "w")
        r4 = open("18936677-k_rodrigo_lave.txt", "w")
        r1.write(self.r1)
        r1.close()
        r2.write(self.r1)
        r2.close()
        r3.write(self.r1)
        r3.close()
        r4.write(self.r1)
        r4.close()
        del self.corr1
        del self.corr2
        del self.corr3
        del self.corr4

    def test_nombre(self):
        self.assertTrue(self.corr1.revisar_nombre())
        self.assertTrue(self.corr2.revisar_nombre())
        self.assertTrue(self.corr3.revisar_nombre())
        self.assertFalse(self.corr4.revisar_nombre())

    def test_formato(self):
        self.assertTrue(self.corr1.revisar_formato(self.corr1.nombre[self.corr1.nombre.rfind(".")+1:]))
        # se espera false pero la funcion esta mala ttxtt
        self.assertFalse(self.corr2.revisar_formato(self.corr2.nombre[self.corr2.nombre.rfind(".")+1:]))
        self.assertTrue(self.corr3.revisar_formato(self.corr3.nombre[self.corr3.nombre.rfind(".")+1:]))
        self.assertTrue(self.corr4.revisar_formato(self.corr4.nombre[self.corr4.nombre.rfind(".")+1:]))

    def test_verificador(self):
        self.assertTrue(self.corr1.revisar_verificador(self.corr1.nombre[:self.corr1.nombre.find("-")+2]))
        self.assertTrue(self.corr2.revisar_verificador(self.corr2.nombre[:self.corr2.nombre.find("-")+2]))
        self.assertTrue(self.corr3.revisar_verificador(self.corr3.nombre[:self.corr3.nombre.find("-")+2]))
        self.assertFalse(self.corr4.revisar_verificador(self.corr4.nombre[:self.corr4.nombre.find("-")+2]))

    def test_orden(self):
        self.assertTrue(self.corr1.revisar_orden(self.corr1.nombre[:self.corr1.nombre.rfind(".")]))
        self.assertTrue(self.corr2.revisar_orden(self.corr2.nombre[:self.corr2.nombre.rfind(".")]))
        self.assertTrue(self.corr3.revisar_orden(self.corr3.nombre[:self.corr3.nombre.rfind(".")]))
        self.assertTrue(self.corr4.revisar_orden(self.corr4.nombre[:self.corr4.nombre.rfind(".")]))

    def test_descontar(self):
        pass

    def test_palabra(self):
        self.assertEquals(self.corr1.get_palabras(),23)
        self.assertEquals(self.corr2.get_palabras(),2262)
        self.assertEquals(self.corr3.get_palabras(),2262)
        self.assertEquals(self.corr4.get_palabras(),23)
    
    def test_descuento(self):
        self.assertEquals(self.corr1.get_descuento(),1)
        self.assertEquals(self.corr2.get_descuento(),0)
        self.assertEquals(self.corr3.get_descuento(),0)
        self.assertEquals(self.corr4.get_descuento(),1.5)



suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
