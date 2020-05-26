from odoo import models, fields, api
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import tools
from odoo.exceptions import UserError

class CreateMedicalReport(models.TransientModel):

    _name = 'create.medical.report'

    patient_id = fields.Many2one('patient.card', string="Patient")#card id
    department_id = fields.Many2one('hr.department', string="Department")
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    disease_id = fields.Many2one('hospital.disease', string = 'Disease')
    date_from = fields.Date('Date From')
    to_date = fields.Date('To Date')

    def _get_op_data(self):
        ops = self.env['hospital.op'].search([])
        return ops
    #onchange
    def _get_op_data_patient(self):
        ops = self.env['hospital.op'].search([('card_id','=',self.patient_id.id)])
        return ops
    def print_report(self):

        data = {
            'model': 'create.medical.report',
            'form': self.read()[0]
        }
        if self.patient_id :
            ops = self._get_op_data_patient()
        else :
            ops = self._get_op_data()


        #All reports(without any filter)
        print("self read",self.read()[0])

        # ops = self._get_op_data()
        ops_list = []
        num = 1
        for o in ops :
            vals = {
                'num':num,
                'seq':o.op_number,
                'date':o.date_op,
                'patient':o.patient_id.name,
                'disease':o.consultation_ids.disease_id.disease_id,
                'doctor':o.doctor_id.name,
                'department':o.doctor_id.department_id.name,
            }
            num += 1
            ops_list.append(vals)

        data['ops']=ops_list
        # return ops


        return self.env.ref('hospital_management.patient_medical_report').report_action(self,data=data)