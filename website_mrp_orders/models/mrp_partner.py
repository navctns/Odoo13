# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpAddPartner(models.Model):
    _inherit = 'mrp.production'

    #check company is true(Test)
    partner_id = fields.Many2one('res.users', string='Partner', check_company=True)
    mrp_order_count = fields.Integer('mrp order count',default = lambda self: self.env['mrp.production'].search_count([('partner_id','=',self.env.user.id)]))

    # @api.depends('moderator_ids')
