from odoo import fields, models, api, exceptions
from odoo.addons import decimal_precision as dp
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from openerp.tools.translate import _ 
import logging

# logger = logging.getLogger(__name__)

class LibraryBook(models.Model): 

    _name = 'library.book' 
    _description = 'Library Book'
    _order = 'date_release desc, name' # sort the records first(from newer to older, then by title)
    # _rec_name = 'short_name' # to use short_name fields as the record representation

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title',translate=True,index=True)
    notes = fields.Text('Internal Notes')
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    # active = fields.Boolean(default=True)
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    author_ids = fields.Many2many('res.partner', string='Authors')
    category_id = fields.Many2one('library.book.category')

    state = fields.Selection(
        [
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ],'State',default="available")

    pages = fields.Integer('Number of Pages',
            groups='base.group_user',
            states={'lost': [('readonly', True)]},
            help='Total book page count', company_dependent=False)
    
    # reader_rating = fields.Float(
    #     'Reader Average Rating',
    #     digits=(14,4), # Optional precision (total, decimals),
    # )

    cost_price = fields.Float(
        'Book Cost', dp.get_precision('Book Price')
    )

    # currency_id = fields.Many2one(
    #     'res.currency', string='Currency'
    # )

    # retail_price = fields.Monetary(
    #     'Retail Price',
    #     # optional: currency_field='currency_id',
    # )

    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        # ondelete='set null',
        # context={},
        # domain=[],
    )

    # publisher_city = fields.Char(
    #     'Publisher City',
    #     related = 'publisher_id.city',
    #     readonly=True
    # )

    # # Computed fields
    # age_days = fields.Float(
    #     string='Days Since Release',
    #     compute='_compute_age',
    #     inverse='_inverse age',
    #     search='_search_age',
    #     # store=False, # optional
    #     # compute_sudo=False #optional
    # )

    #  METHODS 

    # # GIT
    # def make_available(self):
    #     self.ensure_one()
    #     self.state = 'available'

    # # GIT
    # def make_borrowed(self):
    #     self.ensure_one()
    #     self.state = 'borrowed'
    
    # def make_lost(self):
    #     self.ensure_one()
    #     self.state = 'lost'
    #     if not self.env.context.get('avoid_deactivate'):
    #         self.active = False

    # def book_rent(self):
    #     self.ensure_one()

    #     if self.state != 'available':
    #         raise UserError(_('Book is not available for renting'))

    #     rent_as_superuser = self.env['library.book.rent'].sudo()

    #     rent_as_superuser.create({
    #         'book_id': self.id,
    #         'borrow_id': self.env.user.partner_id.id
    #     })
        
    # # GIT
    # def average_book_occupation(self):
    #     sql_query = """
    #         SELECT
    #             lb.name,
    #             avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
    #         FROM
    #             library_book_rent AS lbr
    #         JOIN
    #             library_book as lb ON lb.id = lbr.book_id
    #         WHERE lbr.state = 'returned'
    #         GROUP BY lb.name;"""
    #     self.env.cr.execute(sql_query)
    #     result = self.env.cr.fetchall()
    #     logger.info("Average book occupation: %s", result)

    # # example result: Moby Dick (1851-10-18)
    # def name_get(self):
    #     result = []
    #     for record in self: 
    #         rec_name = "%s (%s)" % (record.name, record.date_release)
    #         result.append((record.id, rec_name))
    #     return result

    # @api.constrains('date_release')
    # def _check_release_date(self):
    #     for record in self:
    #         if record.date_release and record.date_release > fields.Date.today():
    #             raise models.ValidationError('Release date must be in the past')

    # Reference field
    ref_doc_id = fields.Reference(
        selection='_referencable_models', string='Reference Document'
    )
    

    @api.model
    def _referencable_models(self):
        #import pdb; pdb.set_trace
        models = self.env['res.partner'].search([])
        return [(x.id, x.name) for x in models]
    
    # # Method for computed field
    # @api.constrains('date_release')
    # def _compute_age(self):
    #     today = fields.Date.today()
    #     for book in self.filtered('date_release'):
    #         delta = today - book.date_release
    #         book.age_days = delta.days
        
    # # Method for computed field
    # def _inverse_age(self):
    #     today = fields.Date.today()
    #     for book in self.filtered('date_release'):
    #         d = today - timedelta(days=book.age_days)
    #         book.date_release = d 

    # # Method for computed field
    # def _search_age(self, operator, value):
    #     today = fields.Date.today()
    #     value_days = timedelta(days=value)
    #     value_date = today - value_days
    #     # convert with operator:
    #     # book with age > value have a date < value_date
    #     operator_map = {
    #         '>': '<', '>=': '<=',
    #         '<': '>', '<=': '>=',
    #     }
    #     new_op = operator_map.get(operator, operator)
    #     return [('date_release', new_op, value_date)]

    # @api.model
    # def create(self, values):
    #     # import pdb; pdb.set_trace()
    #     if not self.user_has_groups('my_library.acl_book_librarian'):
    #         if 'manager_remarks' in values:
    #             raise UserError(
    #                 'You are not allowed to modify'
    #                 'Manager_remarks'
    #         )
    #     return super(LibraryBook, self).create(values)

    # @api.constrains('cost_price')
    # def _validate_cost_price(self):
    #     if self.cost_price < 0:
    #         raise ValidationError("Price of book cannot be below 0")

    # @api.onchange('state')
    # def on_change_state(self):
    #     import pdb; pdb.set_trace()
    #    
    #     book_id = self._origin.id
    #     book = self.browse(book_id)
    #     if self.state != False:
    #         book.write({'notes': 'HELLOOO'})
    #         #self.description = "lkjsnfdjksndfbsjk"

    
    # def write(self, values):
    #     #import pdb; pdb.set_trace()
    #     if values.get('state', False): 
    #         values['notes'] = "Hello644654"
    #     else:
    #         values['notes'] = "State was false"
    #     return super().write(values)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'
    # count_books = fields.Integer('Number of Authored Books', compute='_compute_count_books')

    published_book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published Books',
    )

    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel' # optional
    )

    # # Methods
    # @api.depends('authored_book_ids')
    # def _compute_count_books(self):
    #     for r in self:
    #         r.count_books = len(r.authored_book_ids)