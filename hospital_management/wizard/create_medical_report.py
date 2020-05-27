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

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if not self.department_id:
            # return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}
            self.department_id = self.doctor_id.department_id
            return {'domain': {'doctor_id': [('job_id', '=', 'Doctor')]}}
        # return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.doctor_id:
            if self.doctor_id.department_id.id != self.department_id.id :
                self.doctor_id = False
        return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}

    #Report filtering
    def _get_op_data(self):
        ops = self.env['hospital.op'].search([])
        return ops
    #onchange
    p = 0
    def _get_op_data_patient(self):
        ops = self.env['hospital.op'].search([('card_id','=',self.patient_id.id)])
        p = 1
        return ops
    def _get_op_data_department(self):
        ops = self.env['hospital.op'].search([('department_id', '=', self.department_id.id)])
        return ops

    def _get_op_data_doctor(self):
        ops = self.env['hospital.op'].search([('doctor_id', '=', self.doctor_id.id)])
        return ops

    def _get_op_data_disease(self):
        # ops = self.env['hospital.op'].search([('disease_id', '=', self.disease_id.id)])
        # return ops
        self.env['create.medical.report'].flush(['disease_id'])
        self.env['hospital.op'].flush(['op_number'])
        self.env['hospital.consult'].flush(['disease_id'])

        query = """SELECT * FROM hospital_op op
                    INNER JOIN hospital_consult consult ON consult.op_no=op.id
                    """
        self._cr.execute(query, [tuple(self.ids)])
        query_res = self._cr.dictfetchall()
        print(query_res)
        ops = []
        num = 1
        for op in query_res:
            if str(op['disease_id']) == str(self.disease_id.id):
                if op['doctor_id']:
                    doctor = self.env['hospital.op'].search([('doctor_id','=',op['doctor_id'])])
                    doc_name = doctor.doctor_id.name
                    dept = doctor.department_id.name
                else :
                    doc_name = ''
                    dept = ''
                if op['patient_id'] :
                    patient = self.env['hospital.op'].search([('patient_id', '=', op['patient_id'])])
                    patient_name = patient.patient_id.name
                else :
                    patient_name = ''
                if op['disease_id'] :
                    disease = self.env['hospital.disease'].search([('id', '=', op['disease_id'])])
                    disease_name = disease.disease_id
                else :

                    disease_name = ''

                vals = {
                    'num': num,
                    'seq': op['op_number'],
                    'date': op['date_op'],
                    'patient': patient_name,
                    'disease': disease_name,
                    'doctor': doc_name,
                    'department': dept,
                }
                num += 1
                ops.append(vals)

            print(op['op_number'])
        return ops


    def _get_op_data_per_date(self):
        if self.date_from :
            ops = self.env['hospital.op'].search([('date_op', '>=', self.date_from)])
            return ops
        if self.to_date :
            ops = self.env['hospital.op'].search([('date_op', '<=', self.to_date)])
            return ops
        if self.to_date and self.date_from :
            ops = self.env['hospital.op'].search(['&',('date_op', '<=', self.to_date),
                                                  ('date_op','>=', self.date_from)])
            return ops
        else :
            ops = self.env['hospital.op'].search([])
            return ops




    def print_report(self):

        data = {
            'model': 'create.medical.report',
            'form': self.read()[0]
        }
        ops_disease = '' #for disease filter only
        if self.patient_id :
            ops = self._get_op_data_patient()
            print(type(ops))
        if self.department_id and not self.doctor_id :
            ops = self._get_op_data_department()

        if self.date_from or self.to_date :
            ops = self._get_op_data_per_date()

        if self.doctor_id :
            ops = self._get_op_data_doctor()

        if self.disease_id :

            ops_disease = self._get_op_data_disease()
            ops = ''
            if self.doctor_id :
                ops_doc = self._get_op_data_doctor()

        else :
            ops = self._get_op_data()


        #All reports(without any filter)
        print("self read",self.read()[0])

        # ops = self._get_op_data()
        ops_list = []
        num = 1
        if ops != '' :
            for o in ops:
                vals = {
                    'num': num,
                    'seq': o.op_number,
                    'date': o.date_op,
                    'patient': o.patient_id.name,
                    'disease': o.consultation_ids.disease_id.disease_id,
                    'doctor': o.doctor_id.name,
                    'department': o.doctor_id.department_id.name,
                }
                num += 1
                ops_list.append(vals)


        #
        if ops_disease != '' :
            data['ops'] = ops_disease
        else :
            data['ops'] = ops_list
        # return ops


        return self.env.ref('hospital_management.patient_medical_report').report_action(self,data=data)