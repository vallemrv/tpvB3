# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from shared.utils import parse_float
import commands
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Comandos(object):
    """docstring for Comandos"""
    def __init__(self):
        super(Comandos, self).__init__()
        self.cortarPapel = chr(29) + chr(86) + chr(1)
        self.agregarLineas = chr(27) + chr(100) + chr(6)
        self.tipoEuro = chr(27) + chr(116) + chr(16)
        self.iniciarImp=chr(27) + chr(64)
        self.resaltado=chr(27) + chr(33) + chr(8)
        self.cortarPapel=chr(29) + chr(86) + chr(1)
        self.centrado=chr(27) + chr(97) + chr(1)
        self.derecha=chr(27) + chr(97) + chr(0)
        self.izquierda=chr(27) + chr(97)+chr(2)
        self.normal=chr(27)+chr(77)+chr(48)
        self.peque=chr(27)+chr(77)+chr(49)
        self.grande=chr(27)+chr(33)+chr(16)
        self.grandeNegrita=chr(27)+chr(33)+chr(24)
        self.abrirCajon=chr(27)+chr(112)+chr(48)
        self.impLogo=chr(28)+chr(112)+chr(1)+chr(48)
        self.saltoLineaFinal =  chr(27)+ chr(74)+ chr(255)
        self.saltoDeLinea = chr(27)+ chr(100)+ chr(1)


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


    def AddNegrita(self):
		self.file.write(self.comandos.resaltado)


    def abrir_cajon(self, nomImp):
        self.file.write(self.comandos.iniciarImp)
        self.file.write(self.comandos.abrirCajon)
        self.file.close()
        commands.getoutput('lpr -P {0} print.aux'.format(nomImp))

    def imprimir(self, nomImp):
        if self.file:
            self.file.write(self.comandos.saltoLineaFinal)
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
        if size == 'peque':
            self.file.write(self.comandos.peque)
        if size == 'grande':
            self.file.write(self.comandos.grande)
        if size == 'normal':
            self.file.write(self.comandos.normal)

    def AddLinea(self, s=None, aling=None, t='normal', negrita=False):
        if aling:
            self.AddALineamiento(aling)

        if negrita and t=='grande':
            self.file.write(self.comandos.grandeNegrita)
        elif negrita and t != 'grande':
            self.AddNegrita()

        self.AddSize(t)

        if s:
            #self.file.write(self.comandos.tipoEuro)
            self.file.write(s)

        self.file.write(self.comandos.saltoDeLinea)
        self.file.write(self.comandos.iniciarImp)

    def imprimirTicket(self, p, num,  lineas, fecha, total):

        self.initDoc()
        self.AddLinea()
        self.AddLinea(s='BTres', aling='centrado', t='grande', negrita=True)
        self.AddLinea(s='Pizzeria y Hamburgeseria', aling='centrado', t='normal', negrita=True)
        self.AddLinea(s='Plaza San lazaro, 9, local 2', aling='centrado', t='peque', negrita=True)
        self.AddLinea(s='NIF: 52527453F', aling='centrado', t='peque', negrita=True)
        self.AddLinea()
        self.AddLinea()
        self.AddLinea(s="     Descripcion                        Total ", aling='centrado')
        self.AddLinea(s="----------------------------------------------", aling='centrado')
        for i in range(len(lineas)):
            l = lineas[i]
            self.AddLinea(s="{0: <35} {1:.2f}".format(l.get('des'), parse_float(l.get('total'))), aling='centrado')
        self.AddLinea(s="Total: {0:.2f}  ".format(parse_float(total)), aling='izq', t='grande')
        self.AddLinea(s="Descuento por inauguracion: {0:.2f}  ".format(parse_float(total)*.5), aling='izq', t='grande')
        self.AddLinea(s=fecha, aling='centrado')
        self.AddLinea()
        self.AddLinea(s="Factura simplificada", aling='centrado')
        self.AddLinea(s="Num: {0}".format(num), aling='centrado')
        self.AddLinea(s="Iva incluido", aling='centrado')
        self.AddLinea()
        self.AddLinea(s="Gracias por su visita", aling='centrado')
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
            l = lineas[i]
            self.AddLinea(s="{0}".format(l.get('des')), aling='centrado', t='grande')
        self.AddLinea()
        self.AddLinea()
        self.AddLinea(s="Avisador num: {0}".format(num), aling='centrado')
        self.AddLinea(s=fecha, aling='centrado')
        self.AddLinea()
        self.AddLinea()
        self.imprimir(p)




if __name__ == '__main__':

    docPrint = DocPrint()
    docPrint.initDoc()
    docPrint.ImprimirLogo()
    docPrint.AddLinea()
    docPrint.AddLinea(s='BTres', aling='centrado', t='grande', negrita=True)
    docPrint.AddLinea(s='Pizzeria y Hamburgeseria', aling='centrado', t='normal', negrita=True)
    docPrint.AddLinea(s='Plaza San lazaro, 9, local 2', aling='centrado', t='peque', negrita=True)
    docPrint.AddLinea(s='NIF: 52527453F', aling='centrado', t='peque', negrita=True)
    docPrint.AddLinea()
    docPrint.AddLinea()
    docPrint.AddLinea(s="Can  Descripcion            Precio   Total", aling='centrado')
    docPrint.AddLinea(s="------------------------------------------", aling='centrado')
    docPrint.AddLinea(s='00000000',aling='centrado')
    docPrint.AddLinea()
    docPrint.AddLinea("Factura simplificada", aling='centrado')
    docPrint.AddLinea(s="Num: {0}".format(0123), aling='centrado')
    docPrint.AddLinea(s="Iva incluido", aling='centrado')
    docPrint.AddLinea()
    docPrint.AddLinea(s="Gracias por su visita", aling='centrado')
    docPrint.AddLinea()


    docPrint.imprimir('caja')
