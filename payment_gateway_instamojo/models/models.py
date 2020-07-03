import logging
import requests

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_repr, float_round
from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')])
    paytrail_key_id = fields.Char(string='Merchant ID', required_if_provider='paytrail', groups='base.group_user')
    # paytrail_merchant_id = fields.Char(string='Merchant ID', required_if_provider='paytrail', groups='base.group_user')

    paytrail_key_secret = fields.Char(string='Merchant Key', required_if_provider='paytrail', groups='base.group_user')

    def stripe_form_generate_values(self, tx_values):
        self.ensure_one()

        base_url = self.get_base_url()
        stripe_session_data = {
            # 'payment_method_types[]': 'card',
            # 'line_items[][amount]': int(
            #     tx_values['amount'] if tx_values['currency'].name in INT_CURRENCIES else float_round(
            #         tx_values['amount'] * 100, 2)),
            # 'line_items[][currency]': tx_values['currency'].name,
            # 'line_items[][quantity]': 1,
            # 'line_items[][name]': tx_values['reference'],
            # 'client_reference_id': tx_values['reference'],
            'success_url': 'url/success',
            'cancel_url': 'url/cancel',
            'merchant_id': '13466',
            'order_number':'123456',
            'params_in':
        }
        tx_values['session_id'] = self._create_stripe_session(stripe_session_data)

        return tx_values


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