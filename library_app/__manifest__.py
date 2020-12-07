# -*- coding: utf-8 -*-
{
    'name': 'Library App',
    'summary': 'App to manage library',
    'website': 'www.example.com',
    'category': 'example category',
    'depends': ['base'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        "views/library_menu.xml",
        "views/library_book.xml",
    ],
    'application': True,
}
