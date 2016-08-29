from main import Alumno, Base, Ramo


class TestSistema:

    def setup_method(self, method):
        self.base = Base()
        self.alumno = Alumno(self.base, 0, "Rodolfo")
        self.ramo = Ramo("MAT9999", "0", "10")
        self.base.db.append(self.ramo)

    # con y sin vacantes
    def test_tomar_si(self):
        assert self.base.inscribir("ICS3902", self.alumno) == True

    def test_tomar_no(self):
        assert self.base.inscribir(self.ramo.sigla, self.alumno) == False

    # ver todas las condiciones de botar
    def test_botar(self):
        cred = self.alumno.creditos_actuales
        largo = len(self.alumno.ramos)
        self.alumno.tomar_ramo("ICS3902")
        for i in self.base.db:
            if i.sigla == "ICS3902":
                aux = i
        self.alumno.botar_ramo("ICS3902")
        assert aux.vacantes == 30 and self.alumno.creditos_actuales == cred and len(self.alumno.ramos) == largo

    # condicion de creditos
    def test_creditos_si(self):
        assert self.alumno.tomar_ramo("ICS3902") == True

    def test_creditos_no(self):
        assert self.alumno.tomar_ramo("IIC2233") == False

    # repeticion de ramos
    def test_repeticion_si(self):
        assert self.alumno.tomar_ramo("ICS3902") == True

    def test_repeticion_no(self):
        self.alumno.tomar_ramo("ICS3902")
        assert self.alumno.tomar_ramo("ICS3902") == False
