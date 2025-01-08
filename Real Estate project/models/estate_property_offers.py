# from dateutil.relativedelta import relativedelta
# from odoo import fields, models, api
# from odoo.exceptions import UserError
# from odoo.tools.translate import _
#
#
# class EstateOffer(models.Model):
#     _name = "estate.property.offer"
#     _description = "Offers made for real estates"
#
#     price = fields.Float()
#     status = fields.Selection(
#         [
#             ("accepted", "Accepted"),
#             ("refused", "Refused"),
#             ("canceled", "Canceled"),
#             ("sold", "Sold"),
#         ],
#         copy=False,
#     )
#     partner_id = fields.Many2one("res.partner", required=True)
#     property_id = fields.Many2one(
#         'estate.property', string='Property', required=True,
#         default=lambda self: self.env['estate.property'].search([], limit=1)  # Example: set a default property
#     )  # Fixed the reference
#     property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)  # Related field for PropertyType
#
#     validity = fields.Integer(default=7)
#     date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
#
#     @api.depends("validity")
#     def _compute_date_deadline(self):
#         for offer in self:
#             offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)
#
#     def _inverse_date_deadline(self):
#         for offer in self:
#             offer.validity = (offer.date_deadline - fields.Date.today()).days
#
#     def action_accept(self):
#         self.ensure_one()
#         if "accepted" in self.property_id.offer_ids.mapped('status'):
#             raise UserError(_("A property can only have one accepted offer."))
#         self.status = "accepted"
#         self.property_id.selling_price = self.price
#
#     def action_refuse(self):
#         for record in self:
#             if record.status == "accepted":
#                 raise UserError(_("You cannot refuse an accepted offer."))
#             record.status = "refused"
#
#     def action_cancel(self):
#         self.ensure_one()
#         if self.status == "sold":
#             raise UserError(_("A sold property cannot be canceled."))
#         if self.status == "accepted":
#             raise UserError(_("You cannot cancel an accepted offer."))
#         self.status = "canceled"
#         return True

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for real estates"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("canceled", "Canceled"),
            ("sold", "Sold"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True,
        default=lambda self: self.env['estate.property'].search([], limit=1)
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)  # Related field for PropertyType

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days


            # -------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EstateOffer, self).create(vals_list)
        for record in records:
            # Ensure property_id is set
            if not record.property_id:
                raise ValidationError("Property is required for the offer.")

            # Update property state if it's 'new'
            if record.property_id.state == "new":
                record.property_id.state = "received"
        return records
    # ----------------------------------------------------------------------------------------------

    def action_accept(self):
        self.ensure_one()


        if self.property_id.state not in ['new', 'received']:
            raise ValidationError(_("Cannot accept an offer for a property not in 'new' or 'received' state."))


        if any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            raise UserError(_("A property can only have one accepted offer."))


        self.status = "accepted"


        self.property_id.selling_price = self.price


        self.property_id.state = 'accepted'

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(_("You cannot refuse an accepted offer."))
            record.status = "refused"

    def action_cancel(self):
        self.ensure_one()
        if self.status == "sold":
            raise UserError(_("A sold property cannot be canceled."))
        if self.status == "accepted":
            raise UserError(_("You cannot cancel an accepted offer."))
        self.status = "canceled"
        return True


