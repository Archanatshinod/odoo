{
    'name': 'Sale order Approval',
    'version':'18.0',
    'sequence': 1,
    'depends':['sale_management'],
    'data':[
            'views/res_config_settings_views.xml',
            'views/sale_order_approvals_views.xml'
    ],
    'application': True,
}