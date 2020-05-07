
from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError




class DoctorFee(models.Model):

    # _name = 'op.doctorfee'
    _inherit = 'hr.employee'

    fee = fields.Integer(string = "Fee", attrs ={'invisible':[('isdoc','=', 0)]})
    isdoc = fields.Integer(default=0, compute = '_compute_isdoc')

    category_ids = fields.Many2many(
        'hr.employee.category', 'op_category_rel',
        'op_id', 'category_id',
        string='Tags')

    @api.depends('job_id')
    def _compute_isdoc(self):
        if self.job_id.name == 'Doctor':
            self.isdoc = 1




