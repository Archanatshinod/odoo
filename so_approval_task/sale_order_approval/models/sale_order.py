from odoo import models, fields, api, _
from odoo.exceptions import UserError

SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('to_approve', 'To Approve'),
    ('approved', 'Approved'),
    ('sent', "Quotation Sent"),
    ('sale', "Sales Order"),
    ('cancel', "Cancelled"),
]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_approval = fields.Boolean(compute='compute_is_approval')
    is_validated = fields.Boolean(compute='compute_is_validated', default=False)
    hide_approve_button = fields.Boolean(compute='compute_hide_approve_button', default=False)
    approver_validate_ids = fields.One2many('sale.approval.validate', 'order_id', readonly=True,
                                            help="Sale Order Approval lines")
    state = fields.Selection(selection=SALE_ORDER_STATE, string="Status", tracking=3, default='draft')
    approved = fields.Boolean(compute='compute_is_fully_approved', default=False)


    @api.depends('approver_validate_ids')
    def compute_hide_approve_button(self):
        """Compute whether to hide the approve button based on the current user's approval status."""
        for rec in self:
            if self.env.user.id not in rec.approver_validate_ids.mapped('approver_id').ids:
                rec.hide_approve_button = True
            else:
                approval_line = rec.approver_validate_ids.filtered(lambda l: not l.is_validated)
                if approval_line and approval_line[0].approver_id.id == self.env.user.id:
                    rec.hide_approve_button = False
                else:
                    rec.hide_approve_button = True

    def compute_is_fully_approved(self):
        """Compute whether the sale order is fully approved."""
        for rec in self:
            approval_line = rec.approver_validate_ids.filtered(lambda l: not l.is_validated)
            rec.approved = not bool(approval_line)

    def compute_is_approval(self):
        """Check whether Sale Order approval is enabled."""
        ICPSudo = self.env['ir.config_parameter'].sudo()
        is_approval = ICPSudo.get_param('sale_order_approval.approvals')
        for rec in self:
            rec.is_approval = bool(is_approval)

    def compute_is_validated(self):
        """Check if the sale order is validated."""
        for rec in self:
            approval_line = rec.approver_validate_ids.filtered(
                lambda l: l.approver_id.id == self.env.user.id and not l.is_validated
            )
            rec.is_validated = bool(approval_line or not rec.approver_validate_ids)

    @api.model
    def create(self, vals):
        """Override create method to assign approvers and set initial state only for orders requiring approval."""
        res = super(SaleOrder, self).create(vals)

        # Proceed only if order requires approval
        if res.is_approval:
            approval = self.env['sale.order.approvals'].search([], order='id desc', limit=1)

            if approval and approval.sale_approver_ids:
                approval_lines = approval.sale_approver_ids.filtered(lambda a: a.is_required)

                approver_data = [(0, 0, {
                    'order_id': res.id,
                    'approver_id': line.approver_id.id,
                    'is_validated': False
                }) for line in approval_lines]

                if approver_data:
                    res.approver_validate_ids = approver_data  # Assign approvers

                    # Notify the first approver
                    first_approver = approval_lines[0].approver_id
                    if first_approver:
                        res.send_approval_mail_notification(approver=first_approver)

        return res  # Ensure the function always returns the created record

    def button_approve(self):
        """Approve the sale order if the current user is an assigned approver."""
        if not self.order_line:
            raise UserError('You need to add a product before approving.')

        user = self.env.user
        user_line = self.approver_validate_ids.search(
            [('is_validated', '=', False), ('order_id', '=', self.id)], order='id asc', limit=1)

        if user_line and user.id == user_line.approver_id.id:
            user_line.is_validated = True
            next_approver = self.approver_validate_ids.search(
                [('is_validated', '=', False), ('order_id', '=', self.id)], order='id asc', limit=1)

            if next_approver:
                self.send_approval_mail_notification(approver=next_approver.approver_id)
            else:
                self.state = 'approved'  # Ensure state is updated only when all approvals are completed

            self.message_post(body=_('Approved this Sale Order'))

        else:
            raise UserError('Other approvals pending.')

    def send_approval_mail_notification(self, approver):
        """Send email notification to the assigned approver."""
        template_id = self.env['ir.model.data']._xmlid_to_res_id(
            'sale_order_approval.mail_notification_approval', raise_if_not_found=False)
        if not template_id:
            return
        values = {
            'object': self,
            'access_link': self._notify_get_action_link('view'),
            'company': self.env.company,
        }
        if approver:
            values.update(assignee_name=approver.sudo().name)
            assignation_msg = self.env['ir.ui.view']._render_template(
                'sale_order_approval.mail_notification_approval', values)
            assignation_msg = self.env['mail.render.mixin']._replace_local_links(assignation_msg)
            self.env["mail.mail"].sudo().create({
                "email_from": self.create_uid.email,
                "body_html": assignation_msg,
                "subject": _('Approval Required'),
                "email_to": approver.email,
                "auto_delete": True,
            }).sudo().send()

    def action_confirm(self):
        """Override confirm method to check for pending approvals before confirming the sale order."""
        for order in self:
            if order.is_approval:
                pending_approvals = order.approver_validate_ids.filtered(lambda a: not a.is_validated)
                if pending_approvals:
                    raise UserError('Approvals pending.')

            # Explicitly set state to 'sale' before confirming
            order.state = 'sale'

        return super(SaleOrder, self).action_confirm()


class SaleApprovalValidate(models.Model):
    _name = 'sale.approval.validate'

    order_id = fields.Many2one('sale.order', required=True)
    approver_id = fields.Many2one('res.users', help="User to approve the sale order")
    is_validated = fields.Boolean(default=False, string='Approved', help="Enabled if the user approved the sale order")
