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
    patient_age=fields.Integer(string="Age")
    patient_gender=fields.Char("Gender")
    patient_blood=fields.Char("Blood Group")
    doctor_id=fields.Many2one("hr.employee",ondelete="set null",string="Doctor",Index=True)
    department_id=fields.Char(string="Department")
    date=fields.Date(string="Date",default=date.today())
    token_no = fields.Char(string='Token No', required=True, copy=False, readonly=True,
                      default='New')

    @api.model

    def create(self, vals):
        if vals.get('token_no', 'New') == 'New':
            vals['token_no'] = self.env['ir.sequence'].next_by_code(
                'op.card') or 'New'
        result = super(OP, self).create(vals)
        return result

    @api.onchange('card_id')

    def _onchange_card_id(self):

        for r in self:
            r.dob=self.card_id.dob
            r.patient_name=self.card_id.patient_id.name
            r.patient_age=self.card_id.age
            r.patient_gender=self.card_id.sex
            r.patient_blood=self.card_id.blood_group

            print(r.dob)

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):

        self.department_id=self.doctor_id.department_id.name