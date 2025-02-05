from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rfq_ids = fields.One2many('purchase.order', 'sale_order_id', string="Related RFQs")
    rfq_count = fields.Integer(string="RFQ Count", compute="_compute_rfq_count")

    @api.depends('rfq_ids')
    def _compute_rfq_count(self):
        """Compute the number of RFQs linked to this sale order."""
        for order in self:
            order.rfq_count = len(order.rfq_ids)


    def action_confirm(self):
        """ Override to create RFQs for each supplier when the sale order is confirmed. """
        res = super(SaleOrder, self).action_confirm()
        purchase_orders = self.create_rfq()
        self.rfq_ids = [(6, 0, purchase_orders.ids)]
        return res

    def create_rfq(self):
        """ Create RFQs for each unique supplier in sale order lines. """
        rfqs = self.env['purchase.order']
        suppliers = self.order_line.mapped('supplier_ids')

        for supplier in suppliers:
            order_lines = self.order_line.filtered(lambda l: supplier in l.supplier_ids)
            if order_lines:
                po_vals = {
                    'partner_id': supplier.id,
                    'sale_order_id': self.id,
                    'order_line': [(0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                    }) for line in order_lines]
                }
                rfq = self.env['purchase.order'].create(po_vals)
                rfqs |= rfq
        return rfqs
    def action_view_rfqs(self):
        """ Open RFQs related to this Sale Order. """
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {'default_sale_order_id': self.id, 'create': False}  # Disable create if necessary
        return action
