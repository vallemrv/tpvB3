# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Feb-2018
# @License: Apache license vesion 2.0


from kivy.event import EventDispatcher
from kivy.properties import StringProperty
import commands
from datetime import datetime

class Comandos(object):
    """docstring for Comandos"""
    def __init__(self):
        super(Comandos, self).__init__()
        self.iniciarImp = chr(27) + chr(64)
        self.agregarLineas = chr(27) + chr(100) + chr(6)
        self.cortarPapel = chr(29) + chr(86) + chr(1)
        self.centrado = chr(27) + chr(97) + chr(1)
        self.derecha = chr(27) + chr(97) + chr(0x02)
        self.izquierda = chr(27) + chr(97)+chr(0x00)
        self.normal = chr(29)+chr(33)+chr(0x00)
        self.mediana = chr(29)+chr(33)+chr(0x11)
        self.grande = chr(29)+chr(33)+chr(0x22)
        self.semigrande = chr(29)+chr(33)+chr(0x02)
        self.negrita = chr(27) + chr(33) + chr(8)
        self.no_negrita = chr(27) + chr(33) + chr(0)
        self.abrirCajon = chr(27) + chr(112) + chr(48)
        self.impLogo = chr(28) + chr(112) + chr(1) + chr(48)
        self.saltoLineaFinal = chr(27) + chr(100) + chr(12)
        self.saltoDeLinea = chr(0xA)

comandos = Comandos()
class DocPrint(EventDispatcher):
    """docstring for DocPrint"""

    def __init__(self, **arg):
        super(DocPrint, self).__init__(**arg)
        self.comandos = Comandos()

    def initDoc(self):
        self.file = open('print.aux', 'w')
        self.file.write(self.comandos.iniciarImp)

    def ImprimirLogo(self):
        self.file.write(self.comandos.impLogo);


    def AddNegritaGrande(self):
		self.file.write(self.comandos.negritaGrande)


    def abrir_cajon(self, nomImp):
        self.file.write(self.comandos.iniciarImp)
        self.file.write(self.comandos.abrirCajon)
        self.file.close()
        commands.getoutput('lpr -P {0} print.aux'.format(nomImp))

    def imprimir(self, nomImp):
        if self.file:
            self.file.write(self.comandos.agregarLineas)
            self.file.write(self.comandos.cortarPapel)
            self.file.close()
            commands.getoutput('lpr -P {0} print.aux'.format(nomImp))

    def AddALineamiento(self, aling):
        if aling == 'centrado':
            self.file.write(self.comandos.centrado)
        if aling == 'der':
            self.file.write(self.comandos.derecha)
        if aling == 'izq':
            self.file.write(self.comandos.izquierda)

    def AddSize(self, size):
        if size == 'normal':
            self.file.write(self.comandos.normal)
        if size == 'mediana':
            self.file.write(self.comandos.mediana)
        if size == 'semigrande':
            self.file.write(self.comandos.semigrande)
        if size == 'grande':
            self.file.write(self.comandos.grande)

    def AddLinea(self, s=None, aling=None, t='normal', negrita=False):
        if aling != None:
           self.AddALineamiento(aling)

        if negrita:
            self.file.write(self.comandos.negrita)
        else:
            self.file.write(self.comandos.no_negrita)

        self.AddSize(t)

        if s != None:
            self.file.write(s)

        self.file.write(self.comandos.saltoDeLinea)

    def imprimirTicket(self, p, num,  lineas, fecha, total,
                        efectivo, cambio, cl=None):

        self.initDoc()
        self.AddLinea()
        self.AddLinea(s='BTres', aling='centrado', t='grande', negrita=True)
        self.AddLinea(s='Pizzeria y Hamburgeseria', aling='centrado',
                      t='mediana', negrita=True)
        self.AddLinea(s='Plaza San lazaro, 9, local 2', aling='centrado',
                      t='normal', negrita=False)
        self.AddLinea(s='NIF: 52527453F', aling='centrado',
                      t='normal', negrita=False)
        self.AddLinea(s='TLF: 958092462', aling='centrado',
                      t='normal', negrita=False)
        self.AddLinea()
        self.AddLinea()
        self.AddLinea(s="Cant  Descripcion                       Total ",
                      aling='centrado')
        self.AddLinea(s="----------------------------------------------",
                      aling='centrado')
        for ln in lineas:
            tipo = ln.tipo if ln.tipo in ("pizzas, burger") else ""
            self.AddLinea(s="{0: >4} {1:>10} {2: >25} {3:.2f} €".format(ln.cant, tipo, ln.text,
                                                      float(ln.total)), aling='centrado', negrita=True)
            des = ln.des.replace(ln.text, "")
            chunks, chunk_size = len(des), 34
            sub = [ des[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
            for s in sub:
                self.AddLinea(s="{0: <4} {1: <35}".format("", s),
                              aling='centrado', negrita=False)


        self.AddLinea(s="Total: {0:0.2f}  ".format(total),
                      aling='izq', t='mediana')
        self.AddLinea(s="Efectivo: {0:0.2f}  ".format(efectivo),
                      aling='izq', t='normal')
        self.AddLinea(s="Cambio: {0:0.2f}  ".format(cambio),
                      aling='izq', t='normal')

        if type(fecha) is datetime:
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")


        self.AddLinea(s=fecha, aling='centrado')
        self.AddLinea()
        self.AddLinea(s="Factura simplificada", aling='centrado')
        self.AddLinea(s="Num: {0}".format(num), aling='centrado')
        self.AddLinea(s="Iva incluido", aling='centrado')
        self.AddLinea()
        self.AddLinea(s="Gracias por su visita", aling='centrado')
        if cl != None and len(cl) > 0:
            self.AddLinea(s="----------------------------------------------",
                          aling='centrado')
            self.AddLinea()
            self.AddLinea(s="----------------------------------------------",
                          aling='centrado')
            cl = cl[0]
            self.AddLinea(s=cl.nombre, aling='der', t="semigrande")
            self.AddLinea(s=cl.direcciones_set.get(query="id=%d"%cl.direccion)[0].direccion,
                          aling='der', t="semigrande")
            self.AddLinea(s=cl.telefono, aling='der',  t="semigrande")
        self.AddLinea()
        self.imprimir(p)

    def printPedido(self, p, num, lineas, fecha, llevar):

        self.initDoc()
        self.AddLinea()
        self.AddLinea(s="Pedido", aling='centrado', t='grande')
        self.AddLinea(s=llevar, aling='centrado', t='grande')
        self.AddLinea(s="----------------------------------------------",
                      aling='centrado', t='grande')
        for i in range(len(lineas)):
            ln = lineas[i]
            self.AddLinea(s="{0}".format(ln.get('des')),
                          aling='centrado', t='grande')
        self.AddLinea()
        self.AddLinea()
        self.AddLinea(s="Avisador num: {0}".format(num), aling='centrado')
        self.AddLinea(s=fecha, aling='centrado')
        self.AddLinea()
        self.AddLinea()
        self.imprimir(p)

    def printDesglose(self, p, fecha, lineas):

        self.initDoc()
        self.AddLinea()
        self.AddLinea(s="Cierre de caja", aling='centrado', t='grande')
        if type(fecha) is datetime:
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")

        self.AddLinea(s=fecha, aling='centrado', t='grande')
        self.AddLinea(s="----------------------------------------------",
                      aling='centrado', t='grande')
        self.AddLinea()
        for linea in lineas:
            can = linea["can"]
            texto_tipo = linea["texto_tipo"]
            tipo = linea["tipo"]
            self.AddLinea(s="Retirar {0: >5} {1} de {2}".format(can,
                                                                texto_tipo,
                                                                tipo),
                          aling='centrado', t='grande')

        self.AddLinea()
        self.AddLinea()
        self.imprimir(p)




if __name__ == '__main__':
    import sys
    import os
    reload(sys)
    sys.setdefaultencoding('UTF8')


    docPrint = DocPrint()
    docPrint.initDoc()
    '''
    #docPrint.ImprimirLogo()
    docPrint.AddLinea()
    docPrint.AddLinea(s='BTres', aling='centrado', t='grande', negrita=True)
    docPrint.AddLinea(s='Pizzeria y Hamburgeseria',
                      aling='centrado', t='normal', negrita=True)
    docPrint.AddLinea(s='Plaza San lazaro, 9, local 2',
                      aling='centrado', t='peque', negrita=True)
    docPrint.AddLinea(s='NIF: 52527453F', aling='centrado',
                      t='peque', negrita=True)
    docPrint.AddLinea()
    docPrint.AddLinea()
    docPrint.AddLinea(s="Can  Descripcion            Precio   Total",
                      aling='centrado')
    docPrint.AddLinea(s="------------------------------------------",
                      aling='centrado')
    docPrint.AddLinea(s='00000000', aling='centrado')
    docPrint.AddLinea()
    docPrint.AddLinea("Factura simplificada", aling='centrado')
    docPrint.AddLinea(s="Num: {0}".format(0123), aling='centrado')
    docPrint.AddLinea(s="Iva incluido", aling='centrado')
    docPrint.AddLinea()
    docPrint.AddLinea(s="Gracias por su visita", aling='centrado')
    docPrint.AddLinea()
    '''


    file = open("logo.bin", "r")
    logo = file.read()

    docPrint.AddLinea(s=comandos.centrado)
    docPrint.AddLinea(s=logo)
    docPrint.AddLinea(s=comandos.negrita)
    docPrint.AddLinea(s=comandos.normal)
    docPrint.AddLinea(s="finger de queso")
    docPrint.AddLinea(s=comandos.no_negrita)
    docPrint.AddLinea(s=comandos.mediana)
    docPrint.AddLinea(s="Raul Blanco")

    docPrint.AddLinea(s=comandos.semigrande)
    docPrint.AddLinea(s="Pepito caracol")

    docPrint.AddLinea(s=comandos.agregarLineas)
    #docPrint.AddLinea(s=chr(0x1D)+"V"+chr(66)+chr(0))
    #docPrint.AddLinea(s=saltoLineaFinal)
    docPrint.AddLinea(s=comandos.cortarPapel)

    docPrint.imprimir('_192_168_0_103')
