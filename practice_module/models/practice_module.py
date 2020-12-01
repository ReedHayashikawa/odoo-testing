from odoo import fields, models


class PracticeClass(models.Model):
    _name = 'practice.module'
    _description = "Practice module description"

    name = fields.Char("Product Name")
    order_dates = fields.Date(string="Order Date")
    notes = fields.Text("Description")
    quantity = fields.Integer("Quantity")
    status = fields.Selection([
                                ('not available', 'Not Available'),
                                ('available', 'Available'),
                                ('progress', 'In Progress')
                                ], 'Status'
                            ) 

    active = fields.Boolean(default=True)