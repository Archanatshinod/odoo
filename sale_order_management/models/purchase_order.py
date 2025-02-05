from odoo import api,fields,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'  # Removed _name

    # Fields
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")

    def button_confirm(self):
        res = super().button_confirm()  # Fixed super call
        remaining_rfqs = self.sale_order_id.rfq_ids.filtered(lambda r: r.state in ['draft', 'sent'] and r.id != self.id)
        remaining_rfqs.button_cancel()
        return res
