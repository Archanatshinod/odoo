# -*- coding: utf-8 -*-
{
    'name': "Sale Order Approval",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'version': '18.0',
    'sequence':1,
    'depends': ['sale_management'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',

        'data/mail_template.xml',
        # views
        'views/sale_order_approvals_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'application':True,
}

