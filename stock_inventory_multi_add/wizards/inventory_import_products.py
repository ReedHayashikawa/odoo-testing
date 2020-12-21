# Copyright 2016 Cédric Pigeon, ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class InventoryImportProducts(models.TransientModel):
    _name = 'inventory.import.products'
    _description = 'Inventory Import Products'

    products = fields.Many2many(comodel_name='product.product')

    # function to store required attributes of a stock inventory line
    @api.model
    def _get_line_values(self, stock, product): 
        #import pdb; pdb.set_trace()
        stock_line = self.env['stock.inventory.line'].new({ 
            'inventory_id': stock.id,
            'location_id': stock.location_id.id, # required
            'product_id': product.id,            # required
            'product_uom_id': product.uom_id.id, # required
        })

        # all functions that are executed based on a 'product_id' change 
        stock_line._compute_theoretical_qty()
        stock_line._onchange_product() 
        stock_line._onchange_quantity_context()

        # writes to the records cache and stores in line_values
        line_values = stock_line._convert_to_write(stock_line._cache) 
        return line_values

    # function to select products and closes window 
    @api.multi
    def select_products(self):
        so_obj = self.env['stock.inventory'] # stock inventory environment
        for wizard in self:
            # browse upon active_id in object and stores
            stock = so_obj.browse(self.env.context.get('active_id', False)) 

            if stock:
                for product in wizard.products:

                    # gets the line values
                    vals = self._get_line_values(stock, product)
                    if vals:

                        # creates a stock inventory line with the value
                        self.env['stock.inventory.line'].create(vals)

        return {'type': 'ir.actions.act_window_close', }