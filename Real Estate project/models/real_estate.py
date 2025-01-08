from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

# class RealEstate(models.Model):
#     _name = "estate.property"
#     _description = "Estate Property"
#
#     active = fields.Boolean(default=True)
#     name = fields.Char(string='Property Name', default="House", required=True)
#     price=fields.Integer()
#     state = fields.Selection(
#         [
#             ("new", "New"),
#             ("received", "Offer Received"),
#             ("accepted", "Offer Accepted"),
#             ("sold", "Sold"),
#             ("canceled", "Canceled")
#         ],
#         required=True,
#         copy=False,
#         default="new"
#     )
#     postcode = fields.Char()
#     date_availability = fields.Date(default=lambda self: fields.Date.today())
#     expected_price = fields.Float()
#     best_offer = fields.Float(compute="_compute_best_offer")
#     selling_price = fields.Float()
#
#     description = fields.Text()
#     bedrooms = fields.Integer()
#     living_area = fields.Integer()
#     facades = fields.Boolean()
#     garage = fields.Boolean()
#     garden = fields.Boolean()
#     garden_area = fields.Integer()
#     total_area = fields.Integer(compute="_compute_total_area")
#     garden_orientation = fields.Selection(
#         [
#             ("north", "North"),
#             ("south", "South"),
#             ("east", "East"),
#             ("west", "West"),
#         ]
#     )
#     property_type_id = fields.Many2one("estate.property.type")
#     buyer_id = fields.Many2one("res.partner", copy=False)
#     salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
#     offer_ids = fields.One2many("estate.property.offer", "property_id")
#     tag_ids = fields.Many2many("estate.property.tag")
#
#     validity = fields.Integer(default=7)
#     date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
#     best_price = fields.Float("Best Offer", compute="_compute_best_price")
#
#     @api.depends("offer_ids.price")
#     def _compute_best_offer(self):
#         for property in self:
#             property.best_offer = max(property.offer_ids.mapped("price")) if property.offer_ids else 0
#
#     @api.depends("living_area", "garden_area")
#     def _compute_total_area(self):
#         for property in self:
#             property.total_area = property.living_area + property.garden_area
#
#     @api.depends("validity")
#     def _compute_date_deadline(self):
#         for property in self:
#             property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)
#
#     def _inverse_date_deadline(self):
#         for property in self:
#             property.validity = (property.date_deadline - fields.Date.today()).days
#
#     @api.onchange("garden")
#     def _onchange_garden(self):
#         for estate in self:
#             if not estate.garden:
#                 estate.garden_area = 0
#
#     @api.onchange("date_availability")
#     def _onchange_date_availability(self):
#         for estate in self:
#             return {
#                 "warning": {
#                     "title": _("Warning"),
#                     "message": _("The availability date has been changed."),
#                 }
#             }
#
#     def action_sold(self):
#         self.ensure_one()
#         if self.state == "canceled":
#             raise UserError(_("A canceled property cannot be sold."))
#         self.state = "sold"
#         return True
#
#     def action_cancel(self):
#         self.ensure_one()
#         if self.state == "sold":
#             raise UserError(_("A sold property can not be canceled"))
#         self.state="canceled"
#         return True
#
#     @api.constrains("selling_price")
#     def _check_constraint(self):
#         for estate in self:
#             if estate.selling_price<5000:
#                 raise ValidationError(_("Test message"))


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    active = fields.Boolean(default=True)
    name = fields.Char(string='Property Name', default="House", required=True)
    price = fields.Integer()
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled")
        ],
        required=True,
        copy=False,
        default="new"
    )
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today())
    expected_price = fields.Float()
    best_offer = fields.Float(compute="_compute_best_offer")
    selling_price = fields.Float()

    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Boolean()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")  # Corrected field name
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price")) if property.offer_ids else 0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for estate in self:
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("The availability date has been changed."),
                }
            }

    def action_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("A canceled property cannot be sold."))
        if self.state == "sold":
            raise UserError(_("This property is already marked as sold."))
        self.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A sold property can not be canceled"))
        self.state = "canceled"
        return True


    @api.constrains("selling_price")
    def _check_constraint(self):
        for estate in self:
            if estate.selling_price < 5000:
                raise ValidationError(_("Selling price must be greater than or equal to 5000"))

