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

    patient_id=fields.Many2one("res.partner",ondelete="set null",string="Patient Name",Index=True)
    dob=fields.Date(string="DOB")
    age=fields.Integer(string="Age")
    sex=fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ],string="Sex")
    address=fields.Text(required=True,string="Address")
    date=fields.Date(string="OP Date",default=datetime.datetime.now())
    phone=fields.Char(string="Telephone")
    mobile=fields.Char(string="Mobile")
    blood_group=fields.Selection([
        ('A+','A+ve'),
        ('B+','B+ve'),
        ('O+','O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')

    ],string="Blood Group")
    seq = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                      default='New')

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
    _description = "Hospital management patent card"

    card_id = fields.Many2one('patient.card',string="Patient Card")
    type = fields.Selection([
        ('OP','OP'),
        ('IP','IP')
    ],string="Consultation Type")
    doctor_id = fields.Many2one('hr.employee')
    date= fields.Date(string = "Date", default = datetime.date.today())
    



