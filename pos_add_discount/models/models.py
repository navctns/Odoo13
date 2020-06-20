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
    discount_perc_amount = fields.Float(string='Discount Percentage amount',
                                        help='The Discount percentage amount to be subracted', )

    discount_product_add = fields.Many2one('product.product', string='Discount Product',
                                          domain="[('available_in_pos', '=', True), ('sale_ok', '=', True)]",
                                          help='The product used to model the discount.')

    @api.onchange('model_id')
    def _onchange_discount_perc_amount(self):
        print('discount percentage amount', self.discount_perc_amount)

    # discount_perc = fields.Float(string='Discount Percentage', help='The Discount percentage',)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    discount_perc_amount = fields.Float(string='Discount Percentage amount', help='The Discount percentage amount to be subracted',)

    @api.onchange('model_id')
    def _onchange_discount_perc_amount(self):
        print('discount percentage amount',self.discount_perc_amount)