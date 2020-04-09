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

class PatientCard(models.Model):
    _name="patient.card"
    _description="Hospital management patent card"

    #name=fields.Char(string="Patient Name",required=True,help="Name of the patient")
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
    #phone = fields.Many2one("res.partner", ondelete="set null", string="Phone", Index=True)
    phone=fields.Char(string="Telephone")
    mobile=fields.Char(string="Mobile")

    bloodgroup=fields.Selection([
        ('A+','A+ve'),
        ('B+','B+ve'),
        ('O+','O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')

    ],string="Blood Group")
    seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    # @api.model
    # def create(self, vals):
    #     if vals.get('seq', _('New')) == _('New'):
    #         seq_date = None
    #         # if 'date_order' in vals:
    #         #     seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
    #         # if 'company_id' in vals:
    #         #     vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
    #         #         'sale.order', sequence_date=seq_date) or _('New')
    #         # else:
    #         vals['seq'] = self.env['ir.sequence'].next_by_code('patient.card', sequence_date=seq_date) or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        # if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
        #     partner = self.env['res.partner'].browse(vals.get('partner_id'))
        #     addr = partner.address_get(['delivery', 'invoice'])
        #     vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
        #     vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
        #     vals['pricelist_id'] = vals.setdefault('pricelist_id',
        #                                            partner.property_product_pricelist and partner.property_product_pricelist.id)
        # result = super(PatientCard, self).create(vals)
        # return result

    #blood_group=fields.Many2one(string="blood group")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):

        self.phone=self.patient_id.phone
        self.mobile=self.patient_id.mobile



