
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
            # 'paytrail_form_url':'https://payment.paytrail.com/api-payment/create'
            # 'paytrail_form_url':  'https: // payment.paytrail.com / api - payment / create'
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

    @api.model
    def paytrail_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        now = datetime.now()
        MID = int(self.paytrail_key_id)
        # url_success = 'http://www.example.com/success'
        url_success = 'http://naveen-vostro-2520:8069/success',
        url_cancel = 'http://naveen-vostro-2520:8069/cancel'
        # url_cancel = 'http://www.example.com/cancel'
        params_in = 'MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,LOCALE'

        # < input
        # name = "PARAMS_IN"
        # type = "hidden"
        # value = "MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,ITEM_TITLE[0],ITEM_ID[0],ITEM_QUANTITY[0],ITEM_UNIT_PRICE[0],ITEM_VAT_PERCENT[0],ITEM_DISCOUNT_PERCENT[0],ITEM_TYPE[0],ITEM_TITLE[1],ITEM_ID[1],ITEM_QUANTITY[1],ITEM_UNIT_PRICE[1],ITEM_VAT_PERCENT[1],ITEM_DISCOUNT_PERCENT[1],ITEM_TYPE[1],MSG_UI_MERCHANT_PANEL,URL_NOTIFY,LOCALE,CURRENCY,REFERENCE_NUMBER,PAYMENT_METHODS,PAYER_PERSON_PHONE,PAYER_PERSON_EMAIL,PAYER_PERSON_FIRSTNAME,PAYER_PERSON_LASTNAME,PAYER_COMPANY_NAME,PAYER_PERSON_ADDR_STREET,PAYER_PERSON_ADDR_POSTAL_CODE,PAYER_PERSON_ADDR_TOWN,PAYER_PERSON_ADDR_COUNTRY,VAT_IS_INCLUDED,ALG" >

        # params_in =

        # order_number = values.get('reference')
        order_number = 12345
        merchant_key = self.paytrail_key_secret

        payment_id = ''
        timestamp = ''
        status = ''
        locale = "en_US"
        params_out = [payment_id, timestamp, status]
        amount = '350'
        hash_key = 'BBDF8997A56F97DC0A46C99C88C2EEF9D541AAD59CFF2695D0DD9AF474086D71'
        item_title = 'Product 101'
        item_unit_price = "300"
        item_vat_prec = '0'

        paytrail_values = dict( values,
        # paytrail_values = dict(

            # MID = int(self.paytrail_key_id),
            MID = 12345,
            # url_success = 'url/payment/success',
            # url_cancel = 'url/payment/cancel',
            url_success = 'http://www.example.com/success',
            url_cancel = 'http://www.example.com/cancel',
            # order_number = values.get('reference'),
            order_number = 12345,
            order_number1 = str(values['reference']),

            # params_in = [MID, url_success, url_cancel, order_number, params_in, params_out ],

                       # < input
        # name = "PARAMS_IN"
        # type = "hidden"
        # value = "MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,ITEM_TITLE[0],ITEM_ID[0],ITEM_QUANTITY[0],ITEM_UNIT_PRICE[0],ITEM_VAT_PERCENT[0],ITEM_DISCOUNT_PERCENT[0],ITEM_TYPE[0],ITEM_TITLE[1],ITEM_ID[1],ITEM_QUANTITY[1],ITEM_UNIT_PRICE[1],ITEM_VAT_PERCENT[1],ITEM_DISCOUNT_PERCENT[1],ITEM_TYPE[1],MSG_UI_MERCHANT_PANEL,URL_NOTIFY,LOCALE,CURRENCY,REFERENCE_NUMBER,PAYMENT_METHODS,PAYER_PERSON_PHONE,PAYER_PERSON_EMAIL,PAYER_PERSON_FIRSTNAME,PAYER_PERSON_LASTNAME,PAYER_COMPANY_NAME,PAYER_PERSON_ADDR_STREET,PAYER_PERSON_ADDR_POSTAL_CODE,PAYER_PERSON_ADDR_TOWN,PAYER_PERSON_ADDR_COUNTRY,VAT_IS_INCLUDED,ALG" >
            params_out = [payment_id, timestamp, status],
            amount='350',
            hash_key = 'BBDF8997A56F97DC0A46C99C88C2EEF9D541AAD59CFF2695D0DD9AF474086D71',
            item_title = 'Product 101',
            item_unit_price = "300",
            item_vat_prec = '0',
            params_in=[MID, url_success, url_cancel, order_number, params_in, params_out, amount, hash_key, item_title, item_unit_price, item_vat_prec],
            # params_in= params_in,
            locale = "en_US",

            currency = 'EUR',
            return_address = 'http://www.example.com/cancel/return',


        )

        # paytm_values['reqHashKey'] = self.generate_checksum(paytm_values,merchant_key)
        # paytm_values['reqHashKey'] = '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ'
        paytrail_values['reqHashKey'] = 'BBDF8997A56F97DC0A46C99C88C2EEF9D541AAD59CFF2695D0DD9AF474086D71'

        r = requests.post(url=self.paytrail_get_form_action_url(), data=paytrail_values)
        print("rrrrrrrrrr :", r)

        # paytm_values_json = json.dumps(paytm_values, indent = 2)
        return paytrail_values

    # r = requests.post(url=paytrail_get_form_action_url(self), data=paytm_values)
    # print("rrrrrrrrrr :", r)

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

    paytrail_txn_type = fields.Char('Transaction type')

    @api.model
    def _paytrail_form_get_tx_from_data(self, data):
        reference = data.get('ORDERID')
        if not reference:
            error_msg = _('Paytm: received data with missing reference (%s)') % (reference)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'Paytm: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    def _paytrail_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if self.acquirer_reference and data.get('mmp_txn') != self.acquirer_reference:
            invalid_parameters.append(('ORDERID', data.get('ORDERID'), self.acquirer_reference))

        return invalid_parameters

    def _paytrail_form_validate(self, data):
        status = data.get('STATUS')
        result = self.write({
            'acquirer_reference': self.env['payment.acquirer'].search([]),
            'date': fields.Datetime.now(),

        })
        if status == 'TXN_SUCCESS':
            self._set_transaction_done()
        elif status != 'TXN_FAILED':
            self._set_transaction_cancel()
        else:
            self._set_transaction_pending()
        return result