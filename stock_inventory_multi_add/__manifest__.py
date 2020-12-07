# Copyright 2016 Cédric Pigeon, ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Stock Inventory Multi Add",
    'summary': """
        Stock Inventory Multi Add """,
    'author': 'ACSONE SA/NV, Odoo Community Association (OCA) (ME)',
    'website': "https://github.com/OCA/sale-workflow",
    'category': 'Inventory Management',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'wizards/inventory_import_products_view.xml',
        'views/inventory_view.xml',
    ],
}
