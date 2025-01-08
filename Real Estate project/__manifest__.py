{
    'name': 'Real Estate',
    'version': '1.3',
    'website': 'https://www.odoo.com',
    # 'depends': ['base'],
    'depends': ['crm','web'],

    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        # Views
        'views/estate_property_views.xml',

        # Menus
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',

        # 'views/estate_property_views.xml',
        # 'views/estate_property_offer_views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}
