from odoo import models, fields

class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'

    borrower_id = fields.Many2one('res.partner', string='Borrower')
    book_ids = fields.Many2many('library.book', string='Books')

    def add_book_rents(self):
        rentModel = self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'borrower_id': wiz.borrower_id.id,
                    'book_id': book.id
                })
        members = self.mapped('borrower_id')
        action = members.get_formview_action()
        if len(borrowers.ids) > 1:
            action['domain'] = [('id', 'in', tuple(members.ids))]
            action['view_mode'] = 'tree,form'
        return action
        
    def _default_member(self):
        if self.context.get('active_model') == 'res.partner':
            return self.context.get('active_id', False)

