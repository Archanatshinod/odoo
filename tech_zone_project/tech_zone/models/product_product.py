from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_online = fields.Float("Stock Online", compute="_compute_stock_levels", store=False)
    stock_offline = fields.Float("Stock Offline", compute="_compute_stock_levels", store=False)

    @api.depends('qty_available')
    def _compute_stock_levels(self):
        """Compute stock levels based on online and offline locations."""
        online_locations = self.env['stock.location'].search([('inventory_type', '=', 'online')])
        offline_locations = self.env['stock.location'].search([('inventory_type', '=', 'offline')])

        for product in self:
            product.stock_online = sum(product.with_context(location=location.id).qty_available for location in online_locations)
            product.stock_offline = sum(product.with_context(location=location.id).qty_available for location in offline_locations)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Override to include stock fields in POS data."""
        data = super()._load_pos_data_fields(config_id)
        data += [
            'stock_online',
            'stock_offline',
        ]
        return data

