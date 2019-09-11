# -*- encoding: utf-8 -*-
##############################################################################
#
#    Globalteckz
#    Copyright (C) 2012 (http://www.globalteckz.com)
#
##############################################################################
__version__ = "1.2.1"

from odoo import api, fields, models
#from odoo.addons.woocommerce_webhook.api.api import API
import datetime
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

class WordpressInstance(models.Model):
    _name = 'wordpress.instance'

    name = fields.Char(string='Name')
    location = fields.Char(string='Location')
    consumer_key = fields.Char(string='Consumer key')
    secret_key=fields.Char(string='Secret Key')
    access_token = fields.Char()
    refresh_token = fields.Char()
    timestamp = fields.Integer()
    redirect_uri = fields.Char(store=False)
    state = fields.Selection([('draft', 'Draft'), ('connected', 'Connected')],string='State', default='draft')
    

# this code is suitable for v2 version.
    @api.multi
    def authorize_oauth(self):
        for rec in self:
            self.create({'name':rec.name,'location':rec.location,'consumer_key':rec.consumer_key,'secret_key':rec.secret_key})
            # Credentials you get from registering a new application
            client_id = rec.consumer_key
            client_secret = rec.secret_key
        
        # OAuth endpoints given in the LinkedIn API documentation
        authorization_base_url = rec.location + '/oauth/authorize'
        token_url = rec.location + '/oauth/token'


        woocommerce = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
        token = woocommerce.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
        self.write({'access_token':token,'state':'connected'})
        #self.write({'state':'connected'})
#            if not r.status_code == 200:
#                raise Warning(("Enter Valid url"))
#            payload1 = {'code':r.code,'client_id':rec.consumer_key,'client_secret':rec.secret_key,'redirect_uri':self.redirect_uri}
#            r1 = requests.post("https://stage.spakat.id/oauth/token",data=payload)
#        self.create({'name':rec.name,'location':rec.location,'consumer_key':rec.consumer_key,'secret_key':rec.secret_key,'access_token':r1.access_token,'refresh_token':r1.refresh_token,'timestamp':int(datetime.datetime.now().timestamp()),'state':'connected'})
