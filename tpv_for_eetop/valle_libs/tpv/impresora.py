# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Mar-2018
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
            print ("Impresora no conectada")



    def printDesglose(self, p, fecha, lineas):

        if type(fecha) is datetime:
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
        else:
            fecha = datetime.strptime(fecha.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")

        try:
            printer = Network(ip_caja, timeout=10)
        except:
            print("Impresora no conectada")
            return False

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
            fecha = datetime.strptime(fecha.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")
            fecha = fecha.strftime("El %a %d-%B a las (%H:%M)")

        try:
            printer = Network(ip_caja, timeout=10)
        except:
            print("Impresora no conectada")
            return False

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
                tipo = ln["tipo"].upper() if ln['tipo'] in ("pizzas, burger") else ""
                if tipo == "":
                    p.writelines("{0: >3} {1: <33} {2:0.2f}".format(ln['cant'], ln['text'],
                                                             float(ln['total'])), align='center',
                                 text_type='bold')
                else:
                    p.writelines("{0: >3} {1: <7} {2: <25} {3:0.2f}".format(ln['cant'], tipo, ln['text'],
                                                             float(ln['total'])), align='center',
                                 text_type='bold')

                if ln['des'].strip() != "":
                    des = ln ['des']
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
                p.writelines(cl['nombre'], align='left', width=2, height=2)

                if "direcciones" in cl:
                    direcciones = cl["direcciones"]
                    text_dir = ""
                    if len(direcciones) > 0:
                        text_dir = direcciones[0]['direccion']
                    for l in direcciones:
                        if cl["direccion"] == l["id"]:
                            text_dir = l["direccion"]
                    p.writelines(text_dir, align='left',width=2, height=2)
                p.writelines("")
                p.writelines(cl['telefono'], align='left', width=2, height=2)
                p.writelines("")
                p.writelines(cl['nota'], align='left', width=2, height=2)
            p.writelines("")
            p.writelines("")
