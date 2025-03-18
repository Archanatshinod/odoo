from odoo import api,fields,models

class SaleOrderApprovals(models.Model):
    _name = 'sale.order.approvals'
    _description = 'Sale order Approvals'

    name=fields.Char(string="name",required=True)
    sale_order_approver_ids=fields.One2many('sale.order.approvers','approval_id')





class SaleOrderApprovers(models.Model):
    _name = 'sale.order.approvers'
    _description = 'Sale order Approvers'

    name=fields.Char(string='name')
    approval_id=fields.Many2one('sale.order.approvals')
    approvers_id=fields.Many2one('res.partner','Approvers')
    is_required=fields.Boolean(string="Is Required")

