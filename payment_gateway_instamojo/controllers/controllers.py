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
            if response.get('id'):
                _logger.info('Paytrail: entering form_feedback with post data %s', pprint.pformat(response))
                request.env['payment.transaction'].sudo().form_feedback(response, 'paytrail')
            #'/payment/process' will give every payment process data
        return '/payment/process'

    @http.route('/web_editor/attachment/add_data', type='json', auth='user', methods=['POST'], website=True)
    def add_data(self, name, data, quality=0, width=0, height=0, res_id=False, res_model='ir.ui.view', filters=False,
                 **kwargs):
        try:
            data = tools.image_process(data, size=(width, height), quality=quality, verify_resolution=True)
        except UserError:
            pass  # not an image
        attachment = self._attachment_create(name=name, data=data, res_id=res_id, res_model=res_model, filters=filters)
        return attachment._get_media_info()