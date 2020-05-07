
from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError




class DoctorFee(models.Model):

    # _name = 'op.doctorfee'
    _inherit = 'hr.employee'

    fee = fields.Monetary(string = "Fee", attrs ={'invisible':[('isdoc','=', 0)]}, currency_field='company_currency')
    isdoc = fields.Integer(default=0, compute = '_compute_isdoc')
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")

    category_ids = fields.Many2many(
        'hr.employee.category', 'op_category_rel',
        'op_id', 'category_id',
        string='Tags')

    @api.depends('job_id')
    def _compute_isdoc(self):
        if self.job_id.name == 'Doctor':
            self.isdoc = 1




