# -*- coding: utf8 -*-
from zlib import compress, decompress, crc32


class InstaPUC:

    @staticmethod
    def getData(filename):
        signature = None
        ihdr = {}
        idat = bytearray()
        iend = None
        with open(filename, "rb") as file:
            signature = bytearray(file.read(8))
            resto = bytearray(file.read())
        largo_chunk = True
        i = 0
        while largo_chunk != 0:
            largo_chunk = int.from_bytes(resto[i + 0:i + 4], byteorder="big")
            tipo_chunk = resto[i + 4:i + 8].decode("utf-8")
            data = resto[i + 8:i + 8 + largo_chunk]
            crc_chunk = resto[i + 8 + largo_chunk:i + 8 + largo_chunk + 4]

            if tipo_chunk == "IHDR":
                ihdr["ancho"] = data[0:4]
                ihdr["alto"] = data[4:8]
                ihdr["profundidad"] = data[8:9]
                ihdr["colores"] = data[9:10]
                ihdr["compresion"] = data[10:11]
                ihdr["filtro"] = data[11:12]
                ihdr["entrelazado"] = data[12:13]

            if tipo_chunk == "IDAT":
                idat = data

            i += 12 + largo_chunk
        return signature, ihdr, decompress(idat), iend

    @staticmethod
    def bytes2matrix(ihdr, idat):
        matriz = []
        fila = []
        ancho = int.from_bytes(ihdr["ancho"], byteorder="big")
        alto = int.from_bytes(ihdr["alto"], byteorder="big")
        for j in range(alto):
            for i in range(ancho):
                aux_1 = idat[1 + j * ancho: 1 + j * ancho + 1]
                aux_2 = idat[1 + j * ancho + 1: 1 + j * ancho + 2]
                aux_3 = idat[1 + j * ancho + 2: 1 + j * ancho + 3]
                aux_1 = int.from_bytes(aux_1, byteorder="big")
                aux_2 = int.from_bytes(aux_2, byteorder="big")
                aux_3 = int.from_bytes(aux_3, byteorder="big")
                fila.append((aux_1, aux_2, aux_3))
            matriz.append(fila)
            fila = []
        return matriz

    @staticmethod
    def matrix2string(matriz):
        """
        Este método transforma la matriz en un string de bytes.
        """
        out = b''
        for i in range(len(matriz)):
            out += (0).to_bytes(1, byteorder='big')
            for j in range(1, len(matriz[i])):
                for k in matriz[i][j]:
                    out += k.to_bytes(1, byteorder='big')
        return out

    @staticmethod
    def rotate(ihdr, matriz):
        sub = []
        girada = []
        for i in range(len(matriz[0])):
            for j in range(len(matriz)):
                sub.append(0)
            girada.append(sub)
            sub = []
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                girada[j][len(girada[0]) - 1 - i] = matriz[i][j]
        return ihdr, girada

    @staticmethod
    def grey(ihdr, matriz):
        salida = []
        sub = []
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                aux = int(
                    (matriz[i][j][0] + matriz[i][j][1] + matriz[i][j][2]) / 3)
                sub.append((aux, aux, aux))
            salida.append(sub)
            sub = []
        ihdr["colores"] = (0).to_bytes(1, byteorder="big")
        return ihdr, salida

    @staticmethod
    def writeImage(outFile, signature, ihdr, idat, iend):
        idat = compress(idat, 9)

        with open(outFile, "wb") as file:
            file.write(signature)
            file.write(ihdr["ancho"])
            file.write(ihdr["alto"])
            file.write(ihdr["profundidad"])
            file.write(ihdr["colores"])
            file.write(ihdr["compresion"])
            file.write(ihdr["filtro"])
            file.write(ihdr["entrelazado"])
            file.write(idat)

        print("Tu imagen ha sido transformada exitosamente!")


if __name__ == '__main__':

    imagefile = 'Mushroom.png'  # Mushroom.png o MickeyMouse.png

    firma, ihdr, data, end = InstaPUC.getData(imagefile)

    matriz = InstaPUC.bytes2matrix(ihdr, data)

    ihdr_gris, matriz_gris = InstaPUC.grey(ihdr, matriz)

    idat_gris = InstaPUC.matrix2string(matriz_gris)

    InstaPUC.writeImage(
        'image.png',
        firma,
        ihdr_gris,
        idat_gris,
        end)


    # Descomentar si se realiza el bonus
    ihdr_gris_rotado, matriz_gris_rotada = InstaPUC.rotate(
        ihdr_gris, matriz_gris)

    idat_gris_rotado = InstaPUC.matrix2string(matriz_gris_rotada)

    InstaPUC.writeImage(
        'image.png',
        firma,
        ihdr_gris_rotado,
        idat_gris_rotado,
        end)

