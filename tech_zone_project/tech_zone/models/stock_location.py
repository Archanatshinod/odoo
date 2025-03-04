from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = ['stock.location']

    inventory_type=fields.Selection([
        ('online', 'Online Inventory'),
        ('offline', 'Offline Inventory')],
        string='Inventory Type', default='offline', required=True)


