# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpAddPartner(models.Model):
    _inherit = 'mrp.production'

    #check company is true(Test)
    partner_id = fields.Many2one('res.partner', string='Partner', check_company=True)
    # mrp_order_count = fields.Integer('mrp order count',compute = "_compute_order_count")

    # @api.depends('moderator_ids')
