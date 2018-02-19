# @Author: Manuel Rodriguez <valle>
# @Date:   07-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 07-Jan-2018
# @License: Apache license vesion 2.0



def vaciar_sesison_subcuentas(request):
    if "accion_pk_subcuenta" in request.session:
        del request.session["accion_pk_subcuenta"]


def vaciar_sesison_cuentas(request):
    if "accion_pk_cuenta" in request.session:
        del request.session["accion_pk_cuenta"]
