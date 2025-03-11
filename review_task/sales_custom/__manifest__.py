{
    'name':'Sale order Customization',
    'version':'18.0',
    'sequence':1,
    'description':'sales with service product',
    'summary':'sales with service product',
    'depends':['sale_management'],
    'data':[
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml'

    ],
    'application': True,
}