from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class OP(models.Model):
    _name="hospital.op"
    _description="Hospital OP"

    card_id = fields.Many2one("patient.card", ondelete ="set null", string="Patient Card", Index=True)
    dob = fields.Date(string = "DOB")
    patient_name = fields.Char(string = "Patient Name")
    patient_age = fields.Integer(string = "Age")
    patient_gender = fields.Char("Gender")
    patient_blood = fields.Char("Blood Group")
    doctor_id = fields.Many2one("hr.employee", ondelete="cascade", string = "Doctor", Index=True
                                , required=True)
    department_id = fields.Char(string = "Department")
    date= fields.Date(string = "Date", default = datetime.date.today())
    op_number = fields.Char(string='OP Number', required=True, copy=False, readonly=True,
                      default='New')
    token_no = fields.Integer(string = 'Token No', default = 1)

    consultation_type = fields.Selection([
        ('OP', 'OP'),
        ('IP', 'IP')
    ], string = "Consultation Type", realated_field = 'hospital.consult.type')

    @api.model

    def create(self, vals):
        if vals.get('op_number', 'New') == 'New':
            vals['op_number'] = self.env['ir.sequence'].next_by_code(
                'op.card') or 'New'
        result = super(OP, self).create(vals)
        return result

    # @api.model
    # def create(self, vals):
    #     if vals.get('token_no', 'New') == 'New':
    #         vals['token_no'] = self.env['ir.sequence'].next_by_id(
    #             self,sequence_date=datetime.date.today()) or 'New'
    #     result = super(OP, self).create(vals)
    #     print('result',result)
    #     return result

    @api.onchange('card_id')

    def _onchange_card_id(self):

        self.token_no += self.token_no + 1

        for r in self:
            r.dob = self.card_id.dob
            r.patient_name = self.card_id.patient_id.name
            r.patient_age = self.card_id.age
            r.patient_gender = self.card_id.sex
            r.patient_blood = self.card_id.blood_group

            print(r.dob)
        for r in self:
            # if r.token_no == self.token_no:
            #     print('same')
            # else:
            #     print('no duplicate')
            print(r)
        #return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):

        # self.department_id = self.doctor_id.department_id.name
        self.department_id = self.doctor_id.department_id.name
        return {'domain': {'doctor_id': [('job_id', 'like', 'Doctor')]}}

    # @api.onchange('card_id')
    # def _onchange_card_id(self):
    #
    #      td = datetime.date.today() #today
    #      mon = td.month
    #      day = td.day
    #
    #      if len(str(mon)) == 1 :
    #          mon = '0' + str(mon)
    #      if len(str(day)) == 1 :
    #          day = '0' + str(day)
    #
    #      td_str = str(td.year)[2:4] + '/' + str(mon) + '/' + str(day)
    #      #print(OP.objects.filter(token_no = 1))
    #      # if td_str == self.op_number[3:11] :
    #      #
    #      #     self.token_no += 1
    #      # else:
    #      #     self.token_no = 1
    #

    @api.model
    def _search_doctor_id(self):

        if self.doctor_id.job_id == "Doctor":

            return self.doctor_id
