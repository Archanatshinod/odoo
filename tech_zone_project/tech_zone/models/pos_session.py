from odoo import api,models

class PosSession(models.Model):
    """Extends the `pos.session` model.
    """
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        data += ['product.product']
        return data
