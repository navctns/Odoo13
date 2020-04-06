# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class new_module_nav(models.Model):
#     _name = 'new_module_nav.new_module_nav'
#     _description = 'new_module_nav.new_module_nav'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Car(models.Model):
    _name="car.car" #name of the model
    description = fields.Text()#newly added

    #create the fields

    name=fields.Char(string="Name")
    horse_power=fields.Integer(string="Horse power")
    door_number=fields.Integer(string="Doors Number")