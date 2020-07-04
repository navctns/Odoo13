
import base64
import string
import random
import hashlib


from Crypto.Cipher import AES
from odoo.exceptions import ValidationError
from odoo import api, fields, models
from datetime import datetime
from werkzeug import urls
import hashlib
import json
import logging
import requests
from paytrail import common

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_repr, float_round
from odoo.addons.payment.models.payment_acquirer import ValidationError
from datetime import datetime

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')])
    paytrail_key_id = fields.Char(string='Merchant ID', required_if_provider='paytrail', groups='base.group_user')
    # paytrail_merchant_id = fields.Char(string='Merchant ID', required_if_provider='paytrail', groups='base.group_user')

    paytrail_key_secret = fields.Char(string='Merchant Key', required_if_provider='paytrail', groups='base.group_user')

    @api.model
    def _get_paytrail_urls(self):
        """ Atom URLS """
        return {
            'paytrail_form_url': 'https://payment.paytrail.com/e2'
        }

    def paytrail_get_form_action_url(self):
        return self._get_paytrail_urls()['paytrail_form_url']

    def _dial(self, method, location, body):
        '''Make the authorization HTTP headers and call the API URL.

        Returns the standard HTTPResponse object.'''

        headers = common.makeHeaders(self.APINAME, common.makeTimestamp(), self.apiKey, self.secret, method, location,
                                     body)
        conn = self.connectionMethod(self.apiLocation)
        conn.request(method, location, body, headers)

        return conn.getresponse()


    def paytrail_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        now = datetime.now()
        MID = int(self.paytrail_key_id)
        url_success = 'http://www.example.com/success'
        url_cancel = 'http://www.example.com/cancel'
        # order_number = values.get('reference')
        order_number = 12345
        merchant_key = self.paytrail_key_secret

        payment_id = ''
        timestamp = ''
        status = ''
        locale = "en_US"

        paytm_values = dict(
        # paytrail_values = dict(

            MID = int(self.paytrail_key_id),
            # url_success = 'url/payment/success',
            # url_cancel = 'url/payment/cancel',
            url_success = 'http://www.example.com/success',
            url_cancel = 'http://www.example.com/cancel',
            # order_number = values.get('reference'),
            order_number = 12345,
            order_number1 = str(values['reference']),
            # params_in = [MID, url_success, url_cancel, order_number, params_in, params_out ],
            params_in=[MID, url_success, url_cancel, order_number, locale],
            locale = "en_US",
            params_out = [payment_id, timestamp,  status],
            amount = '350',

        )

        # paytm_values['reqHashKey'] = self.generate_checksum(paytm_values,merchant_key)
        # paytm_values['reqHashKey'] = '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ'
        paytm_values['reqHashKey'] = 'BBDF8997A56F97DC0A46C99C88C2EEF9D541AAD59CFF2695D0DD9AF474086D71'

        paytm_values_json = json.dumps(paytm_values, indent = 2)
        return paytm_values

    def __encode__(self, to_encode, iv, key):
        __pad__ = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        # Pad
        to_encode = __pad__(to_encode)
        # Encrypt
        c = AES.new(key, AES.MODE_CBC, iv)
        to_encode = c.encrypt(to_encode)
        # Encode
        to_encode = base64.b64encode(to_encode)
        return to_encode.decode("UTF-8")

    def __decode__(self, to_decode, iv, key):
        # Decode
        to_decode = base64.b64decode(to_decode)
        # Decrypt
        c = AES.new(key, AES.MODE_CBC, iv)
        to_decode = c.decrypt(to_decode)
        if type(to_decode) == bytes:
            # convert bytes array to str.
            to_decode = to_decode.decode()
        # remove pad
        return self.__unpad__(to_decode)

    def generate_checksum(self,param_dict ,merchant_key ,salt=None):
        params_string=self.__get_param_string__ (param_dict)
        return self.generate_checksum_by_str (params_string ,merchant_key ,salt)

    def generate_checksum_by_str(self, param_str, merchant_key, salt=None):
        IV = "@@@@&&&&####$$$$"
        params_string = param_str
        salt = salt if salt else self.__id_generator__(4)
        final_string = '%s|%s' % (params_string, salt)

        hasher = hashlib.sha256(final_string.encode())
        hash_string = hasher.hexdigest()

        hash_string += salt

        return self.__encode__(hash_string, IV, merchant_key)




class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _create_paytrail_capture(self, data):
        payment_acquirer = self.env['payment.acquirer'].search([('provider', '=', 'paytrail')], limit=1)
        payment_url = "https://payment.paytrail.com/e2" % (payment_acquirer.paytrail_key_id, payment_acquirer.paytrail_key_secret, data.get('payment_id'))
        try:
            payment_response = requests.get(payment_url)
            payment_response = payment_response.json()
        except Exception as e:
            raise e
        # reference = payment_response.get('notes', {}).get('order_id', False)
        # if reference:
        #     transaction = self.search([('reference', '=', reference)])
        #     capture_url = "https://%s:%s@api.razorpay.com/v1/payments/%s/capture" % (payment_acquirer.razorpay_key_id, payment_acquirer.razorpay_key_secret, data.get('payment_id'))
        #     charge_data = {'amount': int(transaction.amount * 100)}
        #     try:
        #         payment_response = requests.post(capture_url, data=charge_data)
        #         payment_response = payment_response.json()
        #     except Exception as e:
        #         raise e
        return payment_response