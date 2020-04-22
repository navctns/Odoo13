# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


# class hospital_management(models.Model):
#     _name = 'hospital_management.hospital_management'
#     _description = 'hospital_management.hospital_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.valu

class PatientCard(models.Model):
    _name="patient.card"
    _description="Hospital management patent card"
    _rec_name ="seq"

    patient_id=fields.Many2one("res.partner",ondelete="cascade",string="Patient Name",Index=True, required=True)
    dob=fields.Date(string="DOB", required=True)
    age=fields.Integer(string="Age")
    sex=fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ],string="Sex", required=True)
    #address=fields.Text(required=True,string="Address")
    date=fields.Date(string="OP Date",default=datetime.datetime.now())
    phone=fields.Char(string="Telephone")
    mobile=fields.Char(string="Mobile", required=True)
    blood_group=fields.Selection([
        ('A+','A+ve'),
        ('B+','B+ve'),
        ('O+','O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')

    ],string="Blood Group", required=True)
    seq = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                      default='New')
    doctor_id = fields.Char(string ='Doctor')
    department_id = fields.Char(string ="Department" )
    op_number = fields.Many2one(string ="OP No")
    op_date = fields.Date(string = "Date", realated_field ="hospital.op.date")
    op_history_ids = fields.One2many('hospital.op','card_id', string = "OP History")





    @api.model
    def create(self, vals):
        if vals.get('seq', 'New') == 'New':
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'patient.card') or 'New'
        result = super(PatientCard, self).create(vals)
        return result

    @api.onchange('patient_id')
    def _onchange_patient_id(self):

        self.phone=self.patient_id.phone
        self.mobile=self.patient_id.mobile

    @api.onchange('dob')
    def _onchange_dob(self):
        if self.dob:
            year = self.dob.year
            month = self.dob.month
            day = self.dob.day

            if len(str(month)) == 1:
                month = "0" + str(month)
            if len(str(day)) == 1:
                day = "0" + str(day)

            bday = str(year) + "-" + str(month) + "-" + str(day)
            d1=datetime.datetime.strptime(bday,"%Y-%m-%d").date()
            d2 = date.today()
            self.age = relativedelta(d2,d1).years


class Consultation(models.Model):

    _name = "hospital.consult"
    _description = "Hospital management patent consultation"

    card_id = fields.Many2one('patient.card',string="Patient Card", required = True)
    type = fields.Selection([
        ('OP','OP'),
        ('IP','IP')
    ],string = "Consultation Type", required = True)
    op_no = fields.Many2one('hospital.op', string = "OP No", attrs = {'invisible': [('type', 'like', 'IP')]})
    doctor_id = fields.Many2one('hr.employee', required = True)
    date= fields.Date(string = "Date", default = datetime.date.today())
    disease_id = fields.Many2one("hospital.disease", string = "Disease", required = True)
    diagnose = fields.Text(string = "Diagnose", required = True)
    consult_line_ids = fields.One2many("consult.line", 'consult_id', string = "Treatment")

    @api.onchange('type')
    def _onchange_type(self):
    #     # for rec in self:
    #
        if self.type == 'OP' :
    #         # status = 1
            return {'domain': {'op_no': [('card_id', '=', self.card_id.id)]}}
    #         # else return {'domain': {'op_no':[]}}
        elif self.type == 'IP' :
            # self.op_no = 0
            self.op_no = 0
            # self.Hide_product = True
        # if status == 1:
        #     return {'domain': {'op_no': [('card_id', '=', rec.card_id.id)]}}
        # else:
        #     self.op_no = None

    @api.onchange('card_id')
    def _onchange_card_id(self):
        if self.type == 'OP':
            return {'domain': {'op_no': [('card_id', '=', self.card_id.id)]}}
        #         # else return {'domain': {'op_no':[]}}
        elif self.type == 'IP':
            # self.op_no = 0
            self.op_no = 0

    # @api.depends('op_no', 'type')
    # def _compute_op_no(self):
    #     if self.type == 'OP' :
    #         # status = 1
    #         return {'domain': {'op_no': [('card_id', '=', self.card_id.id)]}}
    #     else :
    #         self.op_no = False




class Disease(models.Model):

    _name = "hospital.disease"
    _description = "Disease"

    #desease_id = fields.One2many(string="Disease")
    disease_id = fields.Char(string="Disease")

class ConsultLine(models.Model):

    _name = "consult.line"
    _description = "Disease"

    consult_id = fields.Many2one('hospital.consult', string = "Consult Line")
    medicine = fields.Many2one('product.template', string = "Medicine")
    dose = fields.Char(string = "Dose")
    days = fields.Integer(string = "Days")
    description = fields.Char(string = "Description")








