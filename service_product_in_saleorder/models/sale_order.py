from odoo import api, fields, models

class SaleOrder(models.Model):
    """Extending sale order"""
    _inherit = 'sale.order'

    service_charge_enabled = fields.Boolean(string="Service Charge", default=False)
    service_charge = fields.Float(string="Percentage of Service Charge", default=0.0)
    service_charge_amount = fields.Float(string="Service Charge Amount", default=0.0)

    def action_confirm(self):
        """Override action_confirm to add service charge as an order line"""
        res = super().action_confirm()

        service_product_id = self.env["ir.config_parameter"].sudo().get_param("sales_custom.service_product")
        print("service_product_id", service_product_id)

        if service_product_id:
            service_product = self.env['product.product'].browse(int(service_product_id))
            print("service_product", service_product.name)

        for order in self:
            if order.service_charge_enabled:
                print("order.amount_total",order.amount_total)
                service_charge_amount = order.amount_total * order.service_charge
                print("Service Charge Amount:", service_charge_amount)

                # order.write({'service_charge_amount': service_charge_amount})
                max_sequence = max(order.order_line.mapped('sequence'), default=0)
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id':service_product.id,
                    'price_unit': service_charge_amount,
                    'sequence': max_sequence + 1,
                })
        return res

    # def _create_invoices(self, grouped=False, final=False, date=None):
    #     """Override invoice creation to ensure service charge is included"""
    #     invoices = super()._create_invoices(grouped=grouped, final=final, date=date)
    #
    #     service_product_id = self.env["ir.config_parameter"].sudo().get_param("sales_custom.service_product")
    #
    #     if service_product_id:
    #         service_product = self.env['product.product'].browse(int(service_product_id))
    #
    #     for order in self:
    #         if order.service_charge_enabled and order.service_charge_amount > 0:
    #             # Ensure we create only one service charge line per invoice
    #             self.env['account.move.line'].create({
    #                 'move_id': invoices.id,
    #                 # 'product_id': service_product.id,
    #                 # 'name': "Service Charge",
    #                 'price_unit': order.service_charge_amount,
    #
    #             })

        # return invoices
