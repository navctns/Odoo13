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
    doctor_id = fields.Many2one('hr.employee', string="Doctor",Index=True, domain = {'doctor_id': [('job_id', '=', 'Doctor')]})
    department_id = fields.Many2one('hr.department', string="Department")
    disease_id = fields.Many2one('hospital.disease', string = 'Disease')
    date_from = fields.Date('Date From')
    to_date = fields.Date('To Date')
    report_type = fields.Selection([
        ('pdf','PDF'),
        ('xls','Excel')
    ],string = "Report Format", default='pdf')

    @api.model
    def doctor_domain(self):
        return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        # if not self.department_id:
            # return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}
        self.department_id = self.doctor_id.department_id
        return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}
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
        e = False
        s = True
        label_dt = {
            'date_f': e,
            'date_t': e,
        }
        if self.date_from and not self.to_date:
            ops = self.env['hospital.op'].search([('date_op', '>=', self.date_from)])
            label_dt['date_f'] = s
            return (ops, label_dt)
        if self.to_date and not self.date_from :
            ops = self.env['hospital.op'].search([('date_op', '<=', self.to_date)])
            label_dt['date_t'] = s
            return (ops, label_dt)
        if self.to_date and self.date_from :
            ops = self.env['hospital.op'].search(['&',('date_op', '<=', self.to_date),
                                                  ('date_op','>=', self.date_from)])
            label_dt['date_f'] = s
            label_dt['date_t'] = s
            return (ops, label_dt)
        else :
            ops = self.env['hospital.op'].search([])
            return (ops, label_dt)

    data = {}



    def print_report(self):

        #labels for storing filter criterion in pdf report
        e = '' #empty not selected patient, disease ...
        s = '1'
        label = {
            'patient':e,
            'disease':e,
            'doctor':e,
            'dept':e,
            'date_f':e,
            'date_t':e,
        }
        doc_label =''
        data = {
            'model': 'create.medical.report',
            'form': self.read()[0]
        }
        ops_disease = '' #for disease filter only

        #FIRST METHOD OF FILTERING
        # if self.disease_id :
        #     label['disease'] = s
        #     ops_disease = self._get_op_data_disease()
        #     ops = ''
        #     if self.doctor_id : #doctor filter under disease filter
        #         label['doctor'] = s #doctor is selected
        #         ops_dd = []#disease_doctor
        #         ops_doc = self._get_op_data_doctor()
        #         # ops_disease = ops_disease.search([('doctor_id','=',self.doctor_id.id)])
        #         doc_disease_ids = []
        #         num = 1
        #         for ds in ops_disease :
        #             ops_doc = ops_doc.env['hospital.op'].search(['&',('op_number','=',ds['seq']),
        #                                                          ('doctor_id','=',self.doctor_id.id)])
        #             print('ops doc', ops_doc)
        #             doc_disease_ids.append(ops_doc.id)
        #             print(doc_disease_ids)
        #             ops_doc_id = ops_doc.id
        #             if ops_doc_id:
        #                 doc_name = ops_doc.doctor_id.name
        #                 dept = ops_doc.department_id.name
        #                 patient_name = ops_doc.patient_id.name
        #                 disease_name = self.disease_id.disease_id # recheck
        #                 vals = {
        #                     'num': num,
        #                     'seq': ops_doc.op_number,
        #                     'date': ops_doc.date_op,
        #                     'patient': patient_name,
        #                     'disease': disease_name,
        #                     'doctor': doc_name,
        #                     'department': dept,
        #                 }
        #                 num += 1
        #                 ops_dd.append(vals)
        #
        #         ops_disease = ops_dd
        #
        #         # ops = ops_doc
        # elif self.patient_id :
        #     label['patient'] = s
        #     ops = self._get_op_data_patient()
        #     print(type(ops))
        # elif self.department_id and not self.doctor_id :
        #     label['dept'] = s
        #     ops = self._get_op_data_department()
        #
        # elif self.date_from or self.to_date :
        #
        #     ops, label_dt = self._get_op_data_per_date()
        #     # if self.doctor_id : #doctor filter under disease filter
        #     #     ops_doc = self._get_op_data_doctor()
        #     #     ops = ops.env['hospital.op'].search([('doctor_id','=',self.doctor_id.id)])
        #     label['date_f'] = label_dt['date_f']
        #     label['date_t'] = label_dt['date_t']
        #
        # elif self.doctor_id :
        #     ops = self._get_op_data_doctor()
        #
        # else :
        #     ops = self._get_op_data()
        #
        #
        # #All reports(without any filter)
        # print("self read",self.read()[0])
        #
        # # ops = self._get_op_data()
        # ops_list = []
        # num = 1
        # if ops != '' :
        #     for o in ops:
        #         vals = {
        #             'num': num,
        #             'seq': o.op_number,
        #             'date': o.date_op,
        #             'patient': o.patient_id.name,
        #             'disease': o.consultation_ids.disease_id.disease_id,
        #             'doctor': o.doctor_id.name,
        #             'department': o.doctor_id.department_id.name,
        #         }
        #         num += 1
        #         ops_list.append(vals)
        #
        #
        # #
        # if ops_disease != '' :
        #     data['ops'] = ops_disease
        #     data['label'] = label
        # else :
        #     data['ops'] = ops_list
        #     data['label'] = label
        # # return ops


        #SECOND METHOD OF FILTERING

        ops_doc_ids_1 = []
        ids_pool = []
        ops_dept_ids = []
        ops_patient_ids = []
        ops_list = []
        filter_args = 0
        if self.disease_id :
            label['disease'] = s
            ops_disease = self._get_op_data_disease()
            ops = ''
            if self.doctor_id : #doctor filter under disease filter
                label['doctor'] = s #doctor is selected
                ops_dd = []#disease_doctor
                ops_doc = self._get_op_data_doctor()
                # ops_disease = ops_disease.search([('doctor_id','=',self.doctor_id.id)])
                doc_disease_ids = []
                num = 1
                for ds in ops_disease :
                    ops_doc = ops_doc.env['hospital.op'].search(['&',('op_number','=',ds['seq']),
                                                                 ('doctor_id','=',self.doctor_id.id)])
                    print('ops doc', ops_doc)
                    doc_disease_ids.append(ops_doc.id)
                    ids_pool.append(ops_doc.id) # FILTERING IDS
                    print(doc_disease_ids)
                    ops_doc_id = ops_doc.id
                    if ops_doc_id:
                        doc_name = ops_doc.doctor_id.name
                        dept = ops_doc.department_id.name
                        patient_name = ops_doc.patient_id.name
                        disease_name = self.disease_id.disease_id # recheck
                        vals = {
                            'num': num,
                            'seq': ops_doc.op_number,
                            'date': ops_doc.date_op,
                            'patient': patient_name,
                            'disease': disease_name,
                            'doctor': doc_name,
                            'department': dept,
                        }
                        num += 1
                        ops_dd.append(vals)

                ops_disease = ops_dd

                # ops = ops_doc
        if self.patient_id :
            label['patient'] = s
            ops_patient = self._get_op_data_patient()

            for r in ops_patient:
                ops_patient_ids.append(r.id)
                ids_pool.append(r.id)

            # print(type(ops))
        if self.department_id and not self.doctor_id :
            label['dept'] = s
            ops_dept = self._get_op_data_department()
            for r in ops_dept:
                ops_dept_ids.append(r.id)
                ids_pool.append(r.id)

        if self.date_from or self.to_date :

            ops_date, label_dt = self._get_op_data_per_date()
            # if self.doctor_id : #doctor filter under disease filter
            #     ops_doc = self._get_op_data_doctor()
            #     ops = ops.env['hospital.op'].search([('doctor_id','=',self.doctor_id.id)])
            for r in ops_date:
                ids_pool.append(r.id)
            label['date_f'] = label_dt['date_f']
            label['date_t'] = label_dt['date_t']

        if self.doctor_id :
            ops_doc = self._get_op_data_doctor()
            for r in ops_doc:
                ops_doc_ids_1.append(r.id)
                ids_pool.append(r.id)

        if len(ids_pool) != 0 :
            ids_pool_set = set(ids_pool)#unique ids in filter
            ops_patient_ids_set = set( ops_patient_ids)
            ops_dept_ids_set = set(ops_dept_ids)
            print('patient ids ', ops_patient_ids_set)
            print('dept ids ', ops_dept_ids_set)
            # filtered_ids = list(ids_pool_set)
            filtered_ids = ops_patient_ids_set.intersection(ops_dept_ids_set)
            print('filtered_ids ', filtered_ids)
        if len(filtered_ids) != 0 :
            num = 1
            for i in filtered_ids:  # can be converted to list if wanted
                # if i in ops_dept_ids:
                    o = self.env['hospital.op'].search([('id', '=', i)])
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
                # else:
                #     continue


        # else :
        #     ops = self._get_op_data()
        data['ops'] = ops_list
        #END SECOND METHOD
        if self.report_type == 'xls' :
            return self.env.ref('hospital_management.patient_medical_report_xls').report_action(self, data=data)
        return self.env.ref('hospital_management.patient_medical_report').report_action(self,data=data)


    def print_report_xls(self):
        data = data = {
            'model': 'create.medical.report',
            'form': self.read()[0]
        }
        return self.env.ref('hospital_management.patient_medical_report_xls').report_action(self)

