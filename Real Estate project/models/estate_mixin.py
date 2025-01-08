from odoo import fields, models

class EstateMixin(models.Model):
    _name = "estate.mixin"
    _description = "Mixin Model"

    name = fields.Char(required=True)
