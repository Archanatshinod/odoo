# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Order Management',
    'version': '1.3',
    'summary': 'Manage multiple RFQs within a sale order',
    'sequence': 1,
    'license': 'LGPL-3',
    'depends': ['sale','purchase'],
    'data': [

        'views/sale_order_lines_views.xml',
        'views/sale_order_views.xml'
        # 'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': True,
}

