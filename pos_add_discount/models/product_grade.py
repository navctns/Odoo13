
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductGrade(models.Model):
    _inherit = 'product.template'

    product_grade = fields.Char(string='Product Grade')
