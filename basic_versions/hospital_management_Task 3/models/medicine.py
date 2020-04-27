from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

class Medicine(models.Model):

    _name = 'medicine.product'
    # _inherit = 'product.template'