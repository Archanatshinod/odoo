from odoo import fields, models, api
from odoo.tools.translate import _

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Property Type")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        return res

    def unlink(self):
        for rec in self:
            if rec.property_ids:
                rec.property_ids.write({"state": "cancelled"})
        return super().unlink()

    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act.window",
            "view_mode": "tree,form",
            "res_model": "estate.property",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }
