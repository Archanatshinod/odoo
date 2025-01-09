from odoo import fields, models, api
#
# class ResearchProjectLog(models.Model):
# #     _name = "research.project.log"
# #     _description = "Research Project Change Log"
# #
# #     project_id = fields.Many2one("research.project", string="Project", required=True, ondelete="cascade")
# #     change_summary = fields.Text(string="Change Summary", required=True)
# #     timestamp = fields.Datetime(string="Timestamp", default=fields.Datetime.now, required=True)
#
#
# from odoo import fields, models, api
#
# class ResearchProjectLog(models.Model):
#     _name = "research.project.log"
#     _description = "Research Project Change Log"
#
#     log_ids = fields.One2many(
#         "research.project.log",
#         "project_id",
#         string="Change Logs",
#         help="Logs of changes made to this project."
#     )
#
#     project_id = fields.Many2one(
#         "research.project",
#         string="Project",
#         required=True,
#         ondelete="cascade",
#         help="The research project associated with this log entry."
#     )
#     change_summary = fields.Text(
#         string="Change Summary",
#         required=True,
#         help="A summary of the changes made to the project."
#     )
#     timestamp = fields.Datetime(
#         string="Timestamp",
#         default=fields.Datetime.now,
#         required=True,
#         help="The date and time when this change was logged."
#     )
#
#     _order = "timestamp desc"  # Sort logs by most recent first


class ResearchProjectLog(models.Model):
    _name = "research.project.log"
    _description = "Research Project Change Log"

    project_id = fields.Many2one(
        "research.project",
        string="Project",
        required=True,
        ondelete="cascade",
        help="The research project associated with this log entry."
    )
    change_summary_status = fields.Text(
        string="Updates in status of project",
        required=True,
        help="A summary of the changes made to the project."
    )
    change_summary_assign = fields.Text(
        string=" Updates in assignment of Researchers",
        required=True,
        help="A summary of the changes made to the project."
    )
    timestamp = fields.Datetime(
        string="Timestamp",
        default=fields.Datetime.now,
        required=True,
        help="The date and time when this change was logged."
    )

    _order = "timestamp desc"