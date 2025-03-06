{
    'name':'website_custom',
    'version':'18.0',
    'sequence': 1 ,
    'summary':'website_custom',
    'description': 'website custom',
    'depends':['website','website_sale','stock'],
    'data':[
            'views/templates.xml',
            'views/stock_location_views.xml',
    ],
    'assets':{

    },
    'application': True
}