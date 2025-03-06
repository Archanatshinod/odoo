from odoo import api, fields, models

class ProductProduct(models.Model):
    """
    Extends the 'product.product' model to include stock levels for online
    and offline inventory locations.
    """

    _inherit = "product.product"

    stock_online = fields.Float("Stock Online", compute="_compute_stock_levels", store=False)
    stock_offline = fields.Float("Stock Offline", compute="_compute_stock_levels", store=False)

    @api.depends('qty_available')
    def _compute_stock_levels(self):
        """Compute stock levels based on online and offline locations."""
        online_locations = self.env['stock.location'].search([('inventory_type', '=', 'online')])
        offline_locations = self.env['stock.location'].search([('inventory_type', '=', 'offline')])

        for product in self:
            product.stock_online = 0
            for location in online_locations:
                product.stock_online += product.with_context(location=location.id).qty_available  # Add stock from each online location

            product.stock_offline = 0
            for location in offline_locations:
                product.stock_offline += product.with_context(location=location.id).qty_available  # Add stock from each offline location



