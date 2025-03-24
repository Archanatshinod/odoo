from odoo import models, fields, api

class SaleOrderApprovals(models.Model):
    _name = 'sale.order.approvals'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, help="Name for sale order approval")
    sale_approver_ids = fields.One2many(
        'sale.order.approvers', 'approval_id',
        string="Approvers",
        help="Add users for approving the sale order"
    )


class SaleOrderApprovers(models.Model):
    _name = 'sale.order.approvers'

    approval_id = fields.Many2one(
        'sale.order.approvals', string='Approval',
        required=True, ondelete='cascade'
    )
    sequence = fields.Integer(
        string='Sequence', required=True,
        help="To manage order of approvers"
    )
    approver_id = fields.Many2one(
        'res.users', string='Approver',
        required=True, help="Choose a user to approve the Sale Order"
    )
    is_required = fields.Boolean(
        default=False, string='Is Required',
        help="Enable if approval by the user is required"
    )
