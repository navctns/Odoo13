
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductGrade(models.Model):
    _inherit = 'product.template'

    product_grade = fields.Char(string='Product Grade')



class ProductGradeAdd(models.Model):
    _inherit = 'product.product'

    product_grade = fields.Char(string='Product Grade', related='product_tmpl_id.product_grade')



class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    # types_id = fields.Many2one(related='product_id.product_tmpl_id.types_id',
    #                            string='Product specific type')

    product_grade = fields.Char(string='Product Grade', related='product_id.product_tmpl_id.product_grade')