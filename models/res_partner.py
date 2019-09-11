from odoo import api, fields, models, _
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.exceptions import RequestException

from odoo.addons.component.core import Component
from odoo.addons.component_event.core import EventWorkContext
from odoo.addons.component_event.components.event import skip_if

import json
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = "res.partner"
                
    woo_customer=fields.Boolean('Woocommerce customer',default=False)
    woo_cust_id = fields.Integer('Woocom ID')
    woo_supp_id = fields.Integer('Woocom ID')
    woo_user_status = fields.Char(default='not active')

class VendorEventListener(Component):
    _name = 'vendor.event.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['res.partner']
            
    def on_record_create(self, record, fields=None):
        if record.supplier is True:
            # Get Woocommerce Credential
            webhook = self.env["wordpress.instance"].search([("name","=","wordpress")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            
            # Request Preparation
            url = base_url + "/wp-json/wp/v2/suppliers"
            meta = {"odoo_supp_id":record.id}
            data = {
                "name":record.name,
                "meta":meta
            }
            headers = {
            }
            auth = None
            
            # oAuth 2 endpoint
            authorization_base_url = base_url + '/oauth/authorize'
            token_url = base_url + '/oauth/token'
            
            # Send payload using oAuth2 Session
            woocommerce = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
            token = woocommerce.fetch_token(token_url=token_url, client_id=client_id,
                        client_secret=client_secret)
            headers["Authorization"] = "Bearer " + token["access_token"]
            try:
                response = requests.post(url=url, headers=headers, json=data, auth=auth)
                responseJs = response.json()
                #response = requests.get(url=url, headers=headers, auth=auth)
                record.write({"woo_supp_id":responseJs["id"]})
                _logger.info(responseJs)
            except RequestException:
                _logger.exception(logger_message)
            finally:
                woocommerce.close()
    #@skip_if(lambda self, record, woo_supp_id: woo_supp_id is None)
    def on_record_write(self, record, fields=None):
        if record.supplier is True and record.woo_supp_id is not None:
            # Get Woocommerce Credential
            webhook = self.env["wordpress.instance"].search([("name","=","wordpress")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            
            # Request Preparation
            url = base_url + "/wp-json/wp/v2/suppliers/" + str(record.woo_supp_id)
            data = {
                "name":record.name
            }
            headers = {}
            auth = None
            
            # oAuth 2 endpoint
            authorization_base_url = base_url + '/oauth/authorize'
            token_url = base_url + '/oauth/token'
            
            # Send payload using oAuth2 Session
            woocommerce = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
            token = woocommerce.fetch_token(token_url=token_url, client_id=client_id,
                                            client_secret=client_secret)
            headers["Authorization"] = "Bearer " + token["access_token"]
            try:
                response = requests.post(url=url, headers=headers, json=data, auth=auth)
                #responseJs = response.json()
                #record.write({"woo_supp_id":responseJs["id"]})
                #_logger.info(responseJs["id"])
            except RequestException:
                _logger.exception(logger_message)
            finally:
                woocommerce.close()

        elif record.customer is True and record.woo_cust_id is not None and record.company_type == "company":
                # Get Woocommerce Credential
                webhook = self.env["wordpress.instance"].search([("name","=","wordpress")])
                client_id = webhook.consumer_key
                client_secret = webhook.secret_key
                base_url = webhook.location
                payment_term_id = record.property_payment_term_id.id
                user_roles = {}
                if payment_term_id == 1:
                    data = {
                    "roles":"um_corporate-customer"
                    }
                elif payment_term_id == 2:
                    data = {
                    "roles":"um_corporate-customer-top-14"
                    }
                elif payment_term_id == 3:
                    data = {
                    "roles":"um_corporate-customer-top-30"
                    }
                elif payment_term_id == 4:
                    data = {
                    "roles":"um_corporate-customer-top-3"
                    }
                elif payment_term_id == 5:
                    data = {
                    "roles":"um_corporate-customer-top-7"
                    }
                # Request Preparation
                url = base_url + "/wp-json/wp/v2/users/" + str(record.woo_cust_id)
                headers = {}
                auth = None
            
                # oAuth 2 endpoint
                authorization_base_url = base_url + '/oauth/authorize'
                token_url = base_url + '/oauth/token'
            
                # Send payload using oAuth2 Session
                woocommerce = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
                token = woocommerce.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
                headers["Authorization"] = "Bearer " + token["access_token"]
                try:
                    response = requests.post(url=url, headers=headers, json=data, auth=auth)
                                            #responseJs = response.json()
                                            #record.write({"woo_supp_id":responseJs["id"]})
                                            #_logger.info(responseJs["id"])
                except RequestException:
                    _logger.exception(logger_message)
                finally:
                    woocommerce.close()

    def on_record_unlink(self, record, fields=None):
        if record.supplier is True:
            # Get Woocommerce Credential
            webhook = self.env["wordpress.instance"].search([("name","=","wordpress")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            
            # Request Preparation
            url = base_url + "/wp-json/wp/v2/suppliers/" + str(record.woo_supp_id)
            headers = {}
            params = {"force":True}
            auth = None
            
            # oAuth 2 endpoint
            authorization_base_url = base_url + '/oauth/authorize'
            token_url = base_url + '/oauth/token'
            
            # Send payload using oAuth2 Session
            woocommerce = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
            token = woocommerce.fetch_token(token_url=token_url, client_id=client_id,
                                            client_secret=client_secret)
            headers["Authorization"] = "Bearer " + token["access_token"]
            try:
                response = requests.delete(url=url, headers=headers, params=params, auth=auth)
                #responseJs = response.json()
                #record.write({"woo_supp_id":responseJs["id"]})
                _logger.info(response)
            except RequestException:
                _logger.exception(logger_message)
            finally:
                woocommerce.close()


