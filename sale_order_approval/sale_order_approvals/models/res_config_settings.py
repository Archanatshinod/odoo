from odoo import api,fields,models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_approval=fields.Boolean(string='Approvals',help='Set approvers for sale order validation' )
