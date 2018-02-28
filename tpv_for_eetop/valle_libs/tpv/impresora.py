# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Feb-2018
# @License: Apache license vesion 2.0


from datetime import datetime
from escpos.printer import Network
from escpos.escpos import EscposIO
import locale
import config
import sys

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

ip_caja = config.IP_PRINTER_CAJA

class DocPrint():

    def abrir_cajon(self, *args):
        try:
            printer = Network(ip_caja, timeout=10)
            printer.cashdraw(2)
        except:
            print ("Error en la impresora")



    def printDesglose(self, p, fecha, lineas):

        if type(fecha) is datetime:
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")

        printer = Network(ip_caja, timeout=10)


        with EscposIO(printer) as p:
            p.writelines("Cierre de caja", align='center', width=2, height=2)

            p.writelines(fecha, align='center', width=2, height=2)
            p.writelines("------------------------------------------",
                          align='center')
            p.writelines("")
            for linea in lineas:
                can = linea["can"]
                texto_tipo = linea["texto_tipo"]
                tipo = linea["tipo"]
                p.writelines("Retirar {0: >5} {1} de {2}".format(can, texto_tipo,
                                                                 tipo),height=2,align='center')

            p.writelines("")
            p.writelines("")


    def imprimirTicket(self, p, num,  lineas, fecha, total,
                        efectivo, cambio, cl=None):
        if type(fecha) is datetime:
            fecha = fecha.strftime("El %a %d-%B a las (%H:%M)")
        else:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("El %a %d-%B a las (%H:%M)")

        printer = Network(ip_caja, timeout=10)


        with EscposIO(printer) as p:
            p.printer.set(align='center')
            p.printer.image("logo.png")
            p.writelines("Pizzeria y Hamburgeseria", height=2, width=1, text_type='bold', align='center')
            p.writelines('Plaza San lazaro, 9, local 2', font='a', align='center')
            p.writelines('NIF: 52527453F', font='b', align='center')
            p.writelines('Tlf: 958 092 462', font='b', height=2, width=3, align='center')
            p.writelines('------------------------------------------', align='center')
            p.writelines('FECHA', height=2, width=2, font='a', align='center')
            p.writelines(fecha, height=2, width=1, font='b', align='center')
            p.writelines("Num: %d" % num, text_type='bold',
                         font='a', align='center')
            p.writelines('------------------------------------------', align='center')

            for ln in lineas:
                tipo = ln.tipo if ln.tipo in ("pizzas, burger") else ""
                if tipo == "":
                    p.writelines("{0: >3} {1: <33} {2:0.2f}".format(ln.cant, ln.text,
                                                             float(ln.total)), align='center',
                                 text_type='bold')
                else:
                    p.writelines("{0: >3} {1: <7} {2: <25} {3:0.2f}".format(ln.cant, tipo, ln.text,
                                                             float(ln.total)), align='center',
                                 text_type='bold')
                if ln.des.strip() != "":
                    des = ln.des
                    chunks, chunk_size = len(des), 34
                    sub = [ des[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
                    for s in sub:
                        p.writelines("{0: <36}".format(s), font="a", align='center')

            p.writelines("")
            p.writelines("Total: {0:0.2f}  ".format(total),
                          align='right', height=2)
            p.writelines("Efectivo: {0:0.2f}  ".format(efectivo),
                          align='right')
            p.writelines("Cambio: {0:0.2f}  ".format(cambio),
                          align='right', )


            p.writelines("")
            p.writelines("Factura simplificada",  text_type='bold', height=2, align='center')
            p.writelines("Iva incluido",  text_type='bold', height=2, align='center')
            p.writelines("")
            p.writelines("Gracias por su visita", text_type='bold', height=2, align='center')
            if cl != None and len(cl) > 0:
                p.writelines("------------------------------------------",
                              align='center')
                p.writelines("Datos del cliente", align="center", height=2, text_type='bold')
                p.writelines("------------------------------------------",
                              align='center')
                cl = cl[0]
                p.writelines(cl.nombre, align='left', width=2, height=2)
                p.writelines(cl.direcciones_set.get(query="id=%d"%cl.direccion)[0].direccion,
                              align='left',width=2, height=2)
                p.writelines("")
                p.writelines(cl.telefono, align='left', width=2, height=2)
                p.writelines("")
                p.writelines(cl.nota, align='left', width=2, height=2)
            p.writelines("")
            p.writelines("")



if __name__ == '__main__':
    import sys
    import os
    import locale
    locale.setlocale(locale.LC_TIME, "es_ES") # swedish

    reload(sys)
    sys.setdefaultencoding('UTF8')
    printer = Network(ip_caja)
    fecha = datetime.now().strftime("El %a %d-%B a las (%H:%M)")
    with EscposIO(printer) as p:
        p.writelines('BTres', font='a', height=4, width=4, align='center')
        p.writelines("Pizzeria y Hamburgeseria", height=2, width=1, text_type='bold', align='center')
        p.writelines('Plaza San lazaro, 9, local 2', font='a', align='center')
        p.writelines('NIF: 52527453F', font='b', align='center')
        p.writelines('------------------------------------------', align='center')
        p.writelines('FECHA', height=2, width=2, font='a', align='center')
        p.writelines(fecha, height=2, width=1, font='b', align='center')
        p.writelines('------------------------------------------', align='center')


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
