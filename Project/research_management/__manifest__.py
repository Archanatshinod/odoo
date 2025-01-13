{
    'name': 'research_management',
    'version': '1.3',
    'description': 'This is a web application using Odoo to efficiently manage research projects',
    'depends': ['base', 'mail'],


    'data': [
            # Security
            'security/ir.model.access.csv',

            # # Views
            'views/research_project_views.xml',
            'views/research_researcher_views.xml',

            # Menus
            'views/research_management_menu.xml',
    ],
    'installable': True,
    'application': True,
}
