__author__ = 'nliu'

from apns import APNs, Frame, Payload, PayloadAlert
from pigeon.settings import BASE_DIR


class NotificationHelper(object):
    def __init__(self, device_token):
        self.device_token = device_token
        self.cert_path = BASE_DIR + '/cert.pem'
        self.key_path = BASE_DIR + '/key.pem'

    def send_simple_notification(self, message):
        apns = APNs(use_sandbox=True, cert_file=self.cert_path, key_file=self.key_path)
        payload = Payload(alert=message, sound="default", badge=1)
        apns.gateway_server.send_notification(self.device_token, payload)
        apns.gateway_server.register_response_listener(self.__response_listener)

    def send_notification_with_custome_button(self, message, button_title):
        apns = APNs(use_sandbox=True, cert_file=self.cert_path, key_file=self.key_path)
        alert = PayloadAlert(message, action_loc_key=button_title)
        payload = Payload(alert=alert, sound="default")
        apns.gateway_server.send_notification(self.device_token, payload)
        apns.gateway_server.register_response_listener(self.__response_listener)

    def __response_listener(self, error_response):
        print("client get error-response: " + str(error_response))