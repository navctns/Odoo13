# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    name=fields.Char(string="Patient Name",required=True,help="Name of the patient")
    dob=fields.Date()
    age=fields.Integer(string="Age of the Patient")
    address=fields.Text(required=True)


