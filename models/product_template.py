# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression


class product_template(models.Model):
    _inherit = 'product.template'

    woo_product_id = fields.Integer()
