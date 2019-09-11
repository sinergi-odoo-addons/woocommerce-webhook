# -*- encoding: utf-8 -*-
##############################################################################
#
#    Globalteckz
#    Copyright (C) 2012 (http://www.globalteckz.com)
#
##############################################################################
__version__ = "1.2.1"

from odoo import api, fields, models
from odoo.addons.woocommerce_webhook.api.api import API
import datetime
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

class WoocommerceInstance(models.Model):
    _name = 'woocommerce.instance'

    name = fields.Char(string='Name')
    location = fields.Char(string='Location')
    consumer_key = fields.Char(string='Consumer key')
    secret_key=fields.Char(string='Secret Key')
    state = fields.Selection([('draft', 'Draft'), ('connected', 'Connected')],string='State', default='draft')
    

# this code is suitable for v2 version.
    @api.multi
    def check_connection(self):
        for rec in self:
            wcapi = API(url=rec.location, consumer_key=rec.consumer_key, consumer_secret=rec.secret_key, wp_api=True, version='wc/v3')
            r = wcapi.get("products")
            if not r.status_code == 200:
                raise Warning(("Enter Valid url"))
            rec.write({'state':'connected'})
        return True
