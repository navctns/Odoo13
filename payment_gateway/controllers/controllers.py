# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaytrailController(http.Controller):

    @http.route(['/payment/paytrail/capture'], type='http', auth='public', csrf=False)
    def _create_paytrail_capture(self, **kwargs):
        payment_id = kwargs.get('payment_id')
        if payment_id:
            response = request.env['payment.transaction'].sudo()._create_paytrail_capture(kwargs)
            # if response.get('id'):
            #     _logger.info('Paytrail: entering form_feedback with post data %s', pprint.pformat(response))
            #     request.env['payment.transaction'].sudo().form_feedback(response, 'razorpay')
            #'/payment/process' will give every payment process data
        return '/payment/process'