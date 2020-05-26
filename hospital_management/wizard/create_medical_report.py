from odoo import models, fields, api
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import tools
from odoo.exceptions import UserError

class CreateMedicalReport(models.TransientModel):

    _name = 'create.medical.report'

    patient_id = fields.Many2one('patient.card', string="Patient")
    department_id = fields.Many2one('hr.department', string="Department")
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    disease_id = fields.Many2one('hospital.disease', string = 'Disease')
    date_from = fields.Date('Date From')
    to_date = fields.Date('To Date')

    def _get_op_data(self,data):
        ops = self.env['hospital.appointment'].search([])
        data['ops']=ops

    def print_report(self):
        print("self read",self.read()[0])
        data = {
            'model':'create.medical.report',
            'form' : self.read()[0]
        }

        return self.env.ref('hospital_management.patient_medical_report').report_action(self,data=data)