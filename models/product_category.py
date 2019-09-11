# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _

class product_category(models.Model):
    _inherit = "product.category"
    
    woo_product_cat_id = fields.Integer()
