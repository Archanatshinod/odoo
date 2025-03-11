from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    service_product=fields.Many2one('product.product',string="Service Product",config_parameter="sales_custom.service_product")