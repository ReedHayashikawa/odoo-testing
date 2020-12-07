from odoo import fields, models

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char('Title', required=True)
    date_published = fields.Date()
    isbn = fields.Char('ISBN')
    active = fields.Boolean(default=True)
    cover_image = fields.Binary()

    publisher_id = fields.Many2one('res.partner', string='Publisher')

    author_ids = fields.Many2many('res.partner', string='Authors')


class ResPartner(models.Model):
    _inherit = 'res.partner'


