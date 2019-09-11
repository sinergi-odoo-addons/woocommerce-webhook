# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _

class product_brand(models.Model):
    _inherit = "product.brand"
    
    woo_brand_id = fields.Integer()
