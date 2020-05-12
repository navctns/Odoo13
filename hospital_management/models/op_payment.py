from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class OpPayment(models.Model):
    _name="op.payment"
    _description="OP Payment"
    _inherit = 'account.payment'

    # invoice_ids = fields.Many2many(
    #     'account.payment', 'op_invoice_rel',
    #     'op_inv_id', 'invoice_id',
    #     string='Tags')

    # def action_register_payment(self):
    #     active_ids = self.env.context.get('active_ids')
    #     if not active_ids:
    #         return ''
    #
    #     return {
    #         'name': _('Register Payment'),
    #         'res_model':'account.payment',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('account.view_account_payment_invoice_form').id,
    #         'context': self.env.context,
    #         'target': 'new',
    #         'type': 'ir.actions.act_window',
    #     }




