from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    """ Inheriting ResConfigSettings model"""
    _inherit = 'res.config.settings'

    approvals = fields.Boolean(config_parameter='sale_order_approval.approvals',
                               help="Configuration approvals for the sale order")


