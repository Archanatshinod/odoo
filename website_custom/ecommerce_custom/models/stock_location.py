from odoo import fields, models

class StockLocation(models.Model):
    """
     Extends the 'stock.location' model to introduce an 'inventory_type' field,
     categorizing stock locations as either online or offline.

     This classification enables tracking of product stock levels based on
     their availability in online or offline locations.
    """
    _inherit = ['stock.location']

    inventory_type=fields.Selection([
        ('online', 'Online Inventory'),
        ('offline', 'Offline Inventory')],
        string='Inventory Type', default='offline', required=True)


