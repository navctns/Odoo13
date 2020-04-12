from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class OP(models.Model):
    _name="hospital.op"
    _description="Hospital OP"

    card_id=fields.Many2one("patient.card",ondelete="set null",string="Patient Card",Index=True)
    dob=fields.Date(string="DOB")
    #age=fields.Integer(string="Age")
    @api.onchange('card_id')
    def _onchange_card_id(self):
        self.dob=self.card_id.dob
        print(self.dob)