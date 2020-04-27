from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class Appointment(models.Model):
    _name="hospital.appointment"
    _description="Hospital Appointment"
    # _rec_name = "op_number"

    card_id = fields.Many2one("patient.card", string = "Patient card", required = True)
    patient_name = fields.Char(string = "Patient name")
    doctor_id = fields.Many2one('hr.employee', required = True, domain = [('job_id', 'like', 'Doctor')])
    department_id = fields.Char(string = "Department")
    date = fields.Date(string = "Date", default = fields.Date.today())
    token = fields.Integer(string = 'Token No')
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Draft'),
            ('appointment', 'Appointment'),
            ('op', 'OP'),
        ], default='draft', required=True,
        )

    @api.onchange('card_id')
    def _onchange_card_id(self):
        self.patient_name = self.card_id.patient_id.name

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):

        self.department_id = self.doctor_id.department_id.name

    def action_confirm(self):
        for rec in self:
            rec.state = 'appointment'

    def action_convert_to_op(self):
        self.ensure_one()
        action = {

            'type': 'ir.actions.act_window',
            'card_id': self.card_id,
            'doctor_id': self.doctor_id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'OP Form',
            'view_mode': 'form',
            'res_model': 'hospital.op',
             }

    def action_redirect_to_appointment(self):
        action = self.env.ref('hospital_management.action_patientcard').read()[0]
        # action['domain'] = [('campaign_id', '=', self.id)]
        action['context'] = {'default_card_id': self.card_id.id, 'default_doctor_id': self.doctor_id.id}
        #write return action for appointment with context
        return action