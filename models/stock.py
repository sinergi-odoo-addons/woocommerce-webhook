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

class stockPicking(models.Model):
    _inherit = "stock.picking"
                                   
                                   #woocom_id = fields.Char(string="Woocom ID")
#is_woocom = fields.Boolean(string="Woocom", default=False)

class DeliveryEventListener(Component):
    _name = 'delivery.event.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['stock.picking']
    
    def on_record_write(self, record, fields=None):
        
        if record.picking_type_id.id == 4 and record.state == "done":
            
            # Get Woo Order ID related to delivery
            order = self.env["sale.order"].search([("procurement_group_id","=",record.group_id.id)])
            if order is not None:
                woo_order_id = order.woo_order_id
                woo_order = order.woo_order
                print "======woo_order_id===>",woo_order_id
                print "======woo_order===>",woo_order
            
            if woo_order is True:
                # Get Woocommerce Credential
                webhook = self.env["woocommerce.instance"].search([("name","=","woocommerce")])
                client_id = webhook.consumer_key
                client_secret = webhook.secret_key
                base_url = webhook.location
                status = "completed"
            
                # Request Data Payload Preparation
                data = {
                    "status":status
                }
                wcapi = API(url=base_url, consumer_key=client_id, consumer_secret=client_secret, wp_api=True, version='wc/v3')
                response = wcapi.put("orders/"+str(woo_order_id),data)
