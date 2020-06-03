# -*- coding: utf-8 -*-

from odoo import models, fields, api



class PosAddDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # unsplash_access_key = fields.Char("Access Key", config_parameter='unsplash.access_key')

    discount_type_perc_amt = fields.Selection([
        ('perc','Percentage'),
        ('amount','Amount'),
    ])

class PosConfig(models.Model):
    _inherit = 'pos.config'

    # unsplash_access_key = fields.Char("Access Key", config_parameter='unsplash.access_key')

    discount_type_perc_amount = fields.Selection([
        ('perc','Percentage'),
        ('amount','Amount'),
    ])