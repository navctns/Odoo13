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
    doctor_id = fields.Many2one('hr.employee', string="Doctor",Index=True, domain = [('job_id', '=', 'Doctor')])
    department_id = fields.Many2one('hr.department', string="Department")
    disease_id = fields.Many2one('hospital.disease', string = 'Disease')
    date_from = fields.Date('Date From')
    to_date = fields.Date('To Date')
    report_type = fields.Selection([
        ('pdf','PDF'),
        ('xls','Excel')
    ],string = "Report Format", default='pdf')

    # @api.model
    # def doctor_domain(self):
    #     return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        # if not self.department_id:
            # return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}
        # self.department_id = self.doctor_id.department_id
        if not self.department_id :
            return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}
        # return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}
        # pass
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
        op_disease_ids = []
        for op in query_res:
            if op['disease_id'] == self.disease_id.id:
                op_disease_ids.append(op['id'])
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
                    op_disease_ids.append(disease.id)
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
        return (ops,op_disease_ids)


    def _get_op_data_per_date(self, header_values):

        e = False
        s = True
        label_dt = {
            'date_f': e,
            'date_t': e,
        }
        if self.date_from and not self.to_date:
            ops = self.env['hospital.op'].search([('date_op', '>=', self.date_from)])
            label_dt['date_f'] = s
            #change date format
            from_dt = datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d').strftime('%d/%m/%Y')
            date_to = datetime.datetime.strptime(str(fields.Date.today()), '%Y-%m-%d').strftime('%d/%m/%Y')
            #change date format
            # header_values['from_dt'] = self.date_from
            # header_values['date_to'] = fields.Date.today()
            #pass to dict with changed format
            header_values['from_dt'] = from_dt
            header_values['date_to'] = date_to
            ##########
            return (ops, label_dt, header_values)
        if self.to_date and not self.date_from :
            ops = self.env['hospital.op'].search([('date_op', '<=', self.to_date)])

            label_dt['date_t'] = s#not used
            # header_values['date_to'] = self.to_date
            first_date = self.env['hospital.op'].search([])[0].date_op#get date of first record
            # change date format
            from_dt = datetime.datetime.strptime(str(first_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            date_to = datetime.datetime.strptime(str(self.to_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            # change date format
            header_values['from_dt'] = from_dt
            header_values['date_to'] = date_to
            return (ops, label_dt, header_values)
        if self.to_date and self.date_from :
            ops = self.env['hospital.op'].search(['&',('date_op', '<=', self.to_date),
                                                  ('date_op','>=', self.date_from)])
            label_dt['date_f'] = s
            label_dt['date_t'] = s
            # change date format
            from_dt = datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d').strftime('%d/%m/%Y')
            date_to = datetime.datetime.strptime(str(self.to_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            # change date format
            # header_values['from_dt'] = self.date_from
            # header_values['date_to'] = self.to_date
            header_values['from_dt'] = from_dt
            header_values['date_to'] = date_to
            return (ops, label_dt, header_values)
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
        data['header_vals'] = {}
        ops_disease = '' #for disease filter only
        # header_values =
        #         {'patient': '',
        #          'disease':'',
        #          'doct':'',
        #          'dept':'',
        #          'from_dt':'',
        #          'date_to':''
        #          }
        header_values = {} #empty start can add items

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
        ops_dt_ids = []
        ops_list = []
        doc_disease_ids = []
        filter_args = 0
        field_ptr = [0,0,0,0,0]
        filter_var = {'disease':False, 'patient':False, 'dept':False, 'doct':False, 'dt':False}
        if self.disease_id :
            header_values['disease'] = self.disease_id.disease_id
            label['disease'] = s
            # ops_disease, doc_disease_ids = self._get_op_data_disease()
            # for r in ops_disease :
            #     doc_disease_ids.append(r.id)
            #     ids_pool.append(r.id)
            ids_pool.append(000)
            # filter_var['disease'] = doc_disease_ids
            field_ptr[0] = 1
            consult_op_disease_ids = []
            disease_based_rec = self.env['hospital.op'].search([('consult_count','=', 1)])
            for rec in disease_based_rec :
                if rec.consultation_ids.disease_id == self.disease_id :
                    consult_op_disease_ids.append(rec.id)
                print(rec.id)

            filter_var['disease'] = consult_op_disease_ids
            # ops = ''
            # filter_args += 1
            # if self.doctor_id : #doctor filter under disease filter
            #     label['doctor'] = s #doctor is selected
            #     ops_dd = []#disease_doctor
            #     ops_doc = self._get_op_data_doctor()
            #     # ops_disease = ops_disease.search([('doctor_id','=',self.doctor_id.id)])
            #
            #     num = 1
            #     for ds in ops_disease :
            #         ops_doc = ops_doc.env['hospital.op'].search(['&',('op_number','=',ds['seq']),
            #                                                      ('doctor_id','=',self.doctor_id.id)])
            #         print('ops doc', ops_doc)
            #         doc_disease_ids.append(ops_doc.id)
            #         ids_pool.append(ops_doc.id) # FILTERING IDS
            #         print(doc_disease_ids)
            #         ops_doc_id = ops_doc.id
            #         if ops_doc_id:
            #             doc_name = ops_doc.doctor_id.name
            #             dept = ops_doc.department_id.name
            #             patient_name = ops_doc.patient_id.name
            #             disease_name = self.disease_id.disease_id # recheck
            #             vals = {
            #                 'num': num,
            #                 'seq': ops_doc.op_number,
            #                 'date': ops_doc.date_op,
            #                 'patient': patient_name,
            #                 'disease': disease_name,
            #                 'doctor': doc_name,
            #                 'department': dept,
            #             }
            #             num += 1
            #             ops_dd.append(vals)
            #     ops_disease = ops_dd
            # filter_var['disease'] = doc_disease_ids


                # ops = ops_doc
        if self.patient_id :
            header_values['patient'] = self.patient_id.patient_id.name
            label['patient'] = s
            ops_patient = self._get_op_data_patient()
            filter_args += 1
            field_ptr[1] = 1
            for r in ops_patient:
                ops_patient_ids.append(r.id)
                ids_pool.append(r.id)
            filter_var['patient'] = ops_patient_ids

            # print(type(ops))
        if self.department_id :
            header_values['dept'] = self.department_id.name
            label['dept'] = s
            field_ptr[2] = 1
            ops_dept = self._get_op_data_department()
            for r in ops_dept:
                ops_dept_ids.append(r.id)
                ids_pool.append(r.id)
            filter_args += 1
            filter_var['dept'] = ops_dept_ids #for taking intersection

        if self.doctor_id :
            header_values['doct'] = self.doctor_id.name
            ops_doc = self._get_op_data_doctor()
            for r in ops_doc:
                ops_doc_ids_1.append(r.id)
                ids_pool.append(r.id)
            filter_args += 1
            filter_var['doct']= ops_doc_ids_1
            field_ptr[3] = 1

        if self.date_from or self.to_date :
            ops_date, label_dt, header_values = self._get_op_data_per_date(header_values)
            # if self.doctor_id : #doctor filter under disease filter
            #     ops_doc = self._get_op_data_doctor()
            #     ops = ops.env['hospital.op'].search([('doctor_id','=',self.doctor_id.id)])
            for r in ops_date:
                ops_dt_ids.append(r.id)
                ids_pool.append(r.id)
            label['date_f'] = label_dt['date_f']
            label['date_t'] = label_dt['date_t']
            filter_args += 1
            filter_var['dt'] = ops_dt_ids
            field_ptr[4] = 1
        else :

            all_recs = self.env['hospital.op'].search([])
            l = len(all_recs)
            header_values['from_dt'] = all_recs[0].date_op
            header_values['date_to'] = all_recs[l-1].date_op
            # from_dt,date_to

        all_ops_ids = []
        all_ops = self.env['hospital.op'].search([])
        for r in all_ops :
            all_ops_ids.append(r.id)
            ids_pool.append(000)

        # Method For calculating multiple intersections
        # def set_intersections(fs, argv):
        #     res_filter = []
        #     i = 0
        #     while True:
        #     l = len(argv)
        #     for i in range(l,-1) :
        #         a = argv[i]
        #         res_filter.append(set(arg_ref).intersection(set(arg)))
        #     res_filter = fs.intersection(argv)
        #     res_filter = list(res_filter)
        #     return res_filter

        if len(ids_pool) != 0 :
            ids_pool_set = set(ids_pool)#unique ids in filter
            ops_patient_ids_set = set( ops_patient_ids)
            ops_dept_ids_set = set(ops_dept_ids)
            print('patient ids ', ops_patient_ids_set)
            print('dept ids ', ops_dept_ids_set)
            # filtered_ids = list(ids_pool_set)
            filtered_ids = ops_patient_ids_set.intersection(ops_dept_ids_set)
            # for val in filter_var :
            #     if
            # print('filtered_ids ', filtered_ids)
            filter_arg_rd = list(filter_var.values()) #arguments and data

            #make all lists to sets
            for ls in filter_arg_rd :
                if ls :
                    ls = set(ls)
            print('filter arg rd', filter_arg_rd)
            t_pass = [] # for passing more than one field filters
            first_set = [] #REMINDER
            # filter_arg_rd.remove(None)#empty values not set constraint
            if filter_arg_rd.count(False) == 5 : #no criteria selected
                filtered_ids = all_ops_ids
            # elif len(filter_arg_rd) == 1 :
            elif filter_arg_rd.count(False) == 4 :

                for ls in filter_arg_rd: #one is selected
                    if ls:
                        filtered_ids = ls
                        break
            elif filter_arg_rd.count(False) < 4 : #more than one is selected
                # filter_arg_rd.remove(False)
                # print('false removed:',filter_arg_rd)
                #
                # for v in filter_arg_rd:
                #     if v :
                #         first_set = v
                #         break
                #     if v :
                #         t_pass.append(set(v))
                # t_pass = tuple(t_pass)
                # filtered_ids = set_intersections(set(first_set),t_pass)
                # print('2 var filtered ids',filtered_ids)
                f1 = []#filter 1
                f2 = []
                f3 = []
                f4 = []
                f5 = []
                ptr_list = []
                i_ptr = []
                c = 0
                print('filter dict',filter_var)
                for i in range(len(filter_arg_rd)) :
                    if field_ptr[i] == 1 :
                        print('field ptr ', field_ptr)
                        i_ptr.append(i) #collect that i
                        f1 = filter_arg_rd[i]
                        f1 = set(f1)#filter
                        ptr_list.append(f1)
                        c += 1
                print('field ptr ', field_ptr)
                print('c:', c)
                print('filter args',filter_arg_rd)
                # if 5 - c == 0:
                # if c == 2 :
                #     res_filt = ptr_list[i_ptr[0]].intersection(ptr_list[i_ptr[1]]) #change ptr_list
                # elif c == 3 :
                #     res_filt = ptr_list[i_ptr[0]].intersection(ptr_list[i_ptr[1]],ptr_list[i_ptr[2]])
                #     # for pt in i_ptr :
                # elif c == 4:
                #     res_filt = ptr_list[i_ptr[0]].intersection(ptr_list[i_ptr[1]], ptr_list[i_ptr[2]],ptr_list[i_ptr[3]])
                # elif c == 4:
                #     res_filt = ptr_list[i_ptr[0]].intersection(ptr_list[i_ptr[1]], ptr_list[i_ptr[2]], ptr_list[i_ptr[3]], ptr_list[i_ptr[4]])
                #
                if c == 2 :
                    res_filt = set(filter_arg_rd[i_ptr[0]]).intersection(set(filter_arg_rd[i_ptr[1]])) #change ptr_list
                elif c == 3 :
                    res_filt = set(filter_arg_rd[i_ptr[0]]).intersection(set(filter_arg_rd[i_ptr[1]]),set(filter_arg_rd[i_ptr[2]]))
                    # for pt in i_ptr :
                elif c == 4:
                    res_filt = set(filter_arg_rd[i_ptr[0]]).intersection(set(filter_arg_rd[i_ptr[1]]), set(filter_arg_rd[i_ptr[2]]),set(filter_arg_rd[i_ptr[3]]))
                elif c == 5:
                    res_filt = set(filter_arg_rd[i_ptr[0]]).intersection(set(filter_arg_rd[i_ptr[1]]), set(filter_arg_rd[i_ptr[2]]), set(filter_arg_rd[i_ptr[3]]), set(filter_arg_rd[i_ptr[4]]))


                filtered_ids = list(res_filt)

                    # if field_ptr[i] == 2 :
                    #     f2 = filter_arg_rd[i]
                    #     ptr_list.append(f1)
                    #     c += 1
                    # if field_ptr[i] == 3 :
                    #     f3 = filter_arg_rd[i]
                    # if field_ptr[i] == 4 :
                    #     f4 = filter_arg_rd[i]
                    # if field_ptr[i] == 5 :
                    #     f5 = filter_arg_rd[i]



            # elif len(filter_arg_rd) > 1 :
            #     filtered_ids = set_intersections(filter_arg_rd)


        if len(filtered_ids) != 0 :
            num = 1
            for i in filtered_ids:  # can be converted to list if wanted
                # if i in ops_dept_ids:
                    o = self.env['hospital.op'].search([('id', '=', i)])
                    vals = {
                        'num': num,
                        'seq': o.op_number,
                        # 'date': o.date_op,
                        #change date format to d-m-y
                        'date': datetime.datetime.strptime(str(o.date_op), '%Y-%m-%d').strftime('%d/%m/%Y'),
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
        data['header_vals'] = header_values
        header_values = {}  # empty end can add items(empty the previous)
        # data['header_vals'] = header_values
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

