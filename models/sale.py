# -*- encoding: utf-8 -*-
##############################################################################
#
#    Globalteckz
#    Copyright (C) 2012 (http://www.globalteckz.com)
#
##############################################################################
from odoo import api, fields, models, _
from odoo.addons.woocommerce_webhook.api.api import API
import requests
from requests.exceptions import RequestException
from odoo.addons.component.core import Component
from odoo.addons.component_event.core import EventWorkContext
from odoo.addons.component_event.components.event import skip_if

import sys

sys.setrecursionlimit(2000)

import json
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = "sale.order"
                                   
    woo_order_id =  fields.Integer()
    woo_order=fields.Boolean(default=False)
    woo_order_status = fields.Char()
    woo_order_number = fields.Char()
    sale_type = fields.Char(default='Offline')

class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    
    woo_orderline_id =  fields.Integer()

class OrderEventListener(Component):
    _name = 'order.event.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['sale.order']

    def on_record_write(self, record, fields=None):
        if record.woo_order is True and record.state == "sale":
            # Get Woocommerce Credential
            webhook = self.env["woocommerce.instance"].search([("name","=","woocommerce")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            status = "processing"
            woo_order_id = record.woo_order_id
            
            
            # Request Data Payload Preparation
            data = {
                "status":status
            }
            wcapi = API(url=base_url, consumer_key=client_id, consumer_secret=client_secret, wp_api=True, version='wc/v3')
            response = wcapi.put("orders/"+str(woo_order_id),data)
        elif record.woo_order is True and record.is_order is True and record.state == "cancel":
            # Get Woocommerce Credential
            webhook = self.env["woocommerce.instance"].search([("name","=","woocommerce")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            status = "cancelled"
            woo_order_id = record.woo_order_id
            
            
            # Request Data Payload Preparation
            data = {
                "status":status
            }
            wcapi = API(url=base_url, consumer_key=client_id, consumer_secret=client_secret, wp_api=True, version='wc/v3')
            response = wcapi.put("orders/"+str(woo_order_id),data)
        elif record.woo_order is True and record.is_order is True and record.state == "fm_not_approved":
            # Get Woocommerce Credential
            webhook = self.env["woocommerce.instance"].search([("name","=","woocommerce")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            status = "cancelled"
            woo_order_id = record.woo_order_id
            
            
            # Request Data Payload Preparation
            data = {
                "status":status
            }
            wcapi = API(url=base_url, consumer_key=client_id, consumer_secret=client_secret, wp_api=True, version='wc/v3')
            response = wcapi.put("orders/"+str(woo_order_id),data)
        elif record.woo_order is True and record.state == "quotation_sent" and record.is_order is False:
            # Get Woocommerce Credential
            webhook = self.env["woocommerce.instance"].search([("name","=","woocommerce")])
            client_id = webhook.consumer_key
            client_secret = webhook.secret_key
            base_url = webhook.location
            woo_order_id = record.woo_order_id
            total = record.amount_total
            total_tax = record.amount_tax
            order_line = record.order_line
            line_items = []
            for line in order_line:
                product_product = line.product_id
                product_template = product_product.product_tmpl_id
                woo_product_id = product_template.woo_product_id
                item = {
                    "id":line.woo_orderline_id,
                    "product_id" : woo_product_id,
                    "total" : str(line.price_subtotal),
                    "total_tax" : str(line.price_tax),
                    "quantity" : line.product_uom_qty
                }
                line_items.append(item)
            
            meta_data = [
                {
                    "key":"odoo_quotation_id",
                    "value":record.id
                }
            ]

            # Request Data Payload Preparation
            data = {
                "status":"ywraq-pending",
                "total":str(total),
                "total_tax":str(total_tax),
                "line_items":line_items,
                "meta_data":meta_data
            }
            wcapi = API(url=base_url, consumer_key=client_id, consumer_secret=client_secret, wp_api=True, version='wc/v3')
            response = wcapi.put("orders/"+str(woo_order_id),data)
            log = response.status_code
            _logger.error(data)





