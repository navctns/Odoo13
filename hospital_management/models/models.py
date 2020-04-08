# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


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

class Patient_Card(models.Model):

    _name="patient.card"
    _description="Hospital management patent card"

    #name=fields.Char(string="Patient Name",required=True,help="Name of the patient")
    name=fields.Many2one("res.partner",ondelete="set null",string="Patient",Index=True)
    dob=fields.Date()
    age=fields.Integer(string="Age of the Patient")
    address=fields.Text(required=True)
    date=fields.Date(default=datetime.datetime.now())

    #blood_group=fields.Many2one(string="blood group")



