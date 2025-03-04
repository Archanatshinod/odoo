{
    'name': 'Tech Zone',
    'version': '18.0',
    'sequence': 1,
    'summary': "TechZone, a prominent electronics retailer with both online and multiple physical locations, offers a diverse range of products.",
    'description': 'TechZone, a prominent electronics retailer with both online and multiple physical locations, offers a diverse range of products.',
    'license': 'LGPL-3',
    'depends': ['point_of_sale','stock'],
    'data': [
            'views/view_location_form.xml'
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            #product info popup
            'tech_zone/static/src/xml/product_info_popup.xml',
            'tech_zone/static/src/js/product_info_popup.js',

            #product card
            'tech_zone/static/src/xml/product_card.xml',

            #pop-up for inventory selection
            'tech_zone/static/src/js/product_screen.js',
            'tech_zone/static/src/js/product_inventory_popup.js',
            'tech_zone/static/src/xml/product_inventory_popup.xml'
        ],
    },
    'application': True,
}
