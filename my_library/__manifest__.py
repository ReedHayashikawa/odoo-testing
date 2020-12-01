{
    'name': 'My library',
    'summary': 'Manage books easily',
    'description': "Long description",
    'author': 'Reed Hayashikawa',
    'website': 'www.example.com',
    'version': '12.0.1',
    'depends': ['base', 'decimal_precision'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_views.xml',
        'views/library_book_rent.xml',
        'views/library_book_categ.xml',
        'wizard/library_rent_wizard_form.xml',
        'wizard/library_return_wizard.xml',
        ],
    'demo': ['demo.xml'],
}