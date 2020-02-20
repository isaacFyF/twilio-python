from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class TwilioWrap:

    def __init__(self):
        self.client = self._auth()
        self.services = "XXXXXXXXXXXXX"

    def _auth(self):
        account_sid = "XXXXXXXXXXXXX"
        auth_token = "XXXXXXXXXXXXX"
        client = Client(account_sid, auth_token)

        return client

    def send_sms(self, telefono, channel='sms'):

        data = {
            'error': False,
            'status': "",
            'message': "",
            'code': ""
        }

        try:

            send_verification = self.client.verify.services(self.services).verifications \
                .create(to=telefono, channel=channel)

            data['estado'] = send_verification.status
            data['message'] = self.message_status(send_verification.status)

        except TwilioRestException as e:
            message = self.message_error(e.code)
            data['error'] = True
            data['code'] = e.code
            data['message'] = message

        return data

    def verify_number(self, telefono, code):

        data = {
            'error': False,
            'status': "",
            'message': "",
            'code': ""
        }

        try:

            verification_check = self.client.verify.services(self.services).verification_checks \
                .create(to=telefono, code=code)

            data['estado'] = verification_check.status
            if not verification_check.valid:
                data['message'] = "El codigo de verificacion es incorrecto. Ingresa de nuevo."
            else:
                data['message'] = self.message_status(verification_check.status)

        except TwilioRestException as e:

            message = self.message_error(e.code)
            data['error'] = True
            data['code'] = e.code
            data['message'] = message

        return data


    def message_error(self, error):

        switcher = {
            60202: "Excedio el limite de verificacion intente luego",
            60200: "Telefono incorrecto",
            20404: "Ocurrio un error, codigo esta expirado o es incorrecto, intente de nuevo",
            60203: "Execedio el limite de mensajes enviados intente luego",
            60204: "Servicio no disponible",
            60205: "SMS no es soportado por el telefono",

        }

        return switcher.get(error, 'Ocurrio un error intente mas tarde.')

    def message_status(self, estado):

        switcher = {
            'pending': "Se envio un mensaje de verificacion a su celular verifique",
            'approved': "Verificacion exitosa",
            'denied': "El proceso fue denegado",
            'expired': "El token expiro",
        }

        return switcher.get(estado, 'Ocurrio un error intente mas tarde.')
