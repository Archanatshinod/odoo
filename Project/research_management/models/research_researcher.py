from odoo import fields, models

class Researcher(models.Model):
    """
        The `Researcher` model is used to track information related to researchers working on research projects.
        It includes the researcher's name, email, image, and the projects they are associated with. The model
        allows for many-to-many relationships between researchers and projects.
    """
    _name = "research.researcher"
    _description = "Researcher of research project"

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(attachment=True)
    email = fields.Char(string="Email" ,required=True)
    project_ids = fields.Many2many("research.project","research_project_researcher_rel","researcher_id","project_id",string="Projects")
