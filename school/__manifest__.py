{
    'name': 'School Management',
    'author': 'Damien Bouvy',
    'version': '1.0',
    'license': 'Other OSI approved licence',
    'category': 'School',
    'summary': 'Manage students, classes and all school related stuff!',
    'website': 'https://github.com/PacktPublishing/Mastering-Odoo-12-Development',
    'depends': ['web', 'http_routing'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'views/school_views.xml',
        'views/school_templates.xml',
        'views/assets.xml',
    ],
    'demo': [
        'data/school_demo.xml',
    ],
    'application': True,
    'qweb': [
        "static/src/xml/school.xml",
],
}
