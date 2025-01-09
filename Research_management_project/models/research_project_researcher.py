from odoo import fields, models


class Researcher(models.Model):

    _name = "research.researcher"
    _description = "Researcher of research project"


    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    email = fields.Char(string="Email")
    project_ids = fields.Many2many(
        "research.project",
        "research_project_researcher_rel",
        "researcher_id",
        "project_id",
        string="Projects"
    )
