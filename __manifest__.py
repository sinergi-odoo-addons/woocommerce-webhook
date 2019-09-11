# -*- encoding: utf-8 -*-

{
    "name" : "Odoo 10 Woocommerce Connector",
    "author" : "Sinergi Creative",
    "version" : "10.0.1.8",
    "category" : "Sales",
    "depends" : ['base','account','delivery','stock','sale'],
    "description": """
    Odoo 10 woocommerce connector
    """,
    "data": [
             'views/wocommerce_integration_view.xml',
             'views/wordpress_integration_view.xml',
             #'views/sale_shop_view.xml',
             #'views/woocom_account_view.xml',
             #'views/woocommerce_dashboard_view.xml',
             #'views/order_workflow_view.xml',
             #'views/product_attribute_view.xml',
             #'views/woocom_product_view.xml',
             #'views/res_partner_view.xml',
             #'views/carrier_woocom_view.xml',
             #'views/payment_gatway_view.xml',
             'views/woocom_order_view.xml',
             #'views/stock_view.xml',
             #'views/woocommerce_log_view.xml',
             'views/wocommerce_menus.xml',
      
    ],
    "installable": True,
    "active": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
