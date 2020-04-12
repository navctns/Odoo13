from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class OP(models.Model):
    _name="hospital.op"
    _description="Hospital OP"

    card_id=fields.Many2one("patient.card",ondelete="set null",string="Patient Card",Index=True)
    dob=fields.Date(string="DOB")
    patient_name=fields.Char(string="Patient Name")
    age=fields.Integer(string="Age")
    patient_gender=fields.Char("Gender")
    patient_blood=fields.Char("Blood Group")
    @api.onchange('card_id')
    def _onchange_card_id(self):

        for r in self:
            r.dob=self.card_id.dob
            r.patient_name=self.card_id.patient_id.name
            r.age=self.card_id.age
            r.patient_gender=self.card_id.sex
            r.patient_blood=self.card_id.blood_group

            print(r.dob)