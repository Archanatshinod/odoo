from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    supplier_ids = fields.Many2many(
        'res.partner',
        string='Suppliers',

    )
