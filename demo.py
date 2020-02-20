# -*- coding: utf-8 -*-
import sys
from wrap_twilio import TwilioWrap


if __name__ == "__main__":
    telefono = str(input('Introduce el telefono como string con el codigo de pais Ejemplo(+56923456789)!: '))
    tw = TwilioWrap()
    result = tw.send_sms(telefono)
    print result
    if not result.get('error', True):
        print "Se envio un codigo al numero {}".format(telefono)
        codigo = str(input('Ingrese el codigo enviado al celular {}: '.format(telefono)))
        print tw.verify_number(telefono, codigo)