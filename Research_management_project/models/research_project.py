# from odoo import fields, models, api
# from odoo.exceptions import ValidationError
#
# class ResearchProject(models.Model):
#     _name = "research.project"
#     _description = "Research Project Model"
#
#     # Fields
#     name = fields.Char(string='Project Name', default="Project Name", required=True)
#     start_date = fields.Date(default=lambda self: fields.Date.today())
#     end_date = fields.Date(default=lambda self: fields.Date.today())
#     duration = fields.Integer(compute='_compute_duration', store=True, string='Duration (in days)')
#
#     # Researcher_id
#     researcher_ids = fields.Many2many("research.researcher", string="Researchers")
#
#     # Project summary
#     project_summary = fields.Text(string="Project Summary",help="Provide a brief description of the project’s goals, milestones, and outcomes.")
#
#     #status
#     status = fields.Selection([('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed'),('cancelled', 'Cancelled')],default='New',string="Status")
#
#     #log_ids
#     log_ids = fields.One2many("research.project.log", "project_id", string="Logs")
#
#     # Compute duration
#     @api.depends("start_date", "end_date")
#     def _compute_duration(self):self
#         for research in self:
#             if research.start_date and research.end_date:
#                 delta = research.end_date - research.start_date
#                 research.duration = delta.days
#             else:
#                 research.duration = 0
#
#     # Validation for end_date
#     @api.constrains("start_date", "end_date")
#     def _check_dates(self):
#         for research in self:
#             if research.end_date < research.start_date:
#                 raise ValidationError("The end date cannot be earlier than the start date.")
#
#
#
#
#     # tracking log and progress
#         # Override write to track changes
#         def write(self, vals):
#             for record in self:
#                 changes = []
#                 # Track status change
#                 if "status" in vals and vals["status"] != record.status:
#                     changes.append(f"Status changed from '{record.status}' to '{vals['status']}'")
#
#                 # Track researcher assignments
#                 if "researcher_ids" in vals:
#                     old_researchers = set(record.researcher_ids.mapped("name"))
#                     new_researchers = set(
#                         self.env["research.researcher"].browse(vals["researcher_ids"][0][2]).mapped("name"))
#                     added = new_researchers - old_researchers
#                     removed = old_researchers - new_researchers
#                     if added:
#                         changes.append(f"Researchers added: {', '.join(added)}")
#                     if removed:
#                         changes.append(f"Researchers removed: {', '.join(removed)}")
#
#                 # Create logs for changes
#                 if changes:
#                     self.env["research.project.log"].create({
#                         "project_id": record.id,
#                         "change_summary": "\n".join(changes)
#                     })
#
#             return super(ResearchProject, self).write(vals)
#
#         # Override create to track initial values
#         @api.model
#         def create(self, vals):
#             record = super(ResearchProject, self).create(vals)
#             changes = [f"Project created with status '{vals.get('status', 'new')}'"]
#             if "researcher_ids" in vals:
#                 researchers = self.env["research.researcher"].browse(vals["researcher_ids"][0][2]).mapped("name")
#                 changes.append(f"Researchers assigned: {', '.join(researchers)}")
#             self.env["research.project.log"].create({
#                 "project_id": record.id,
#                 "change_summary": "\n".join(changes)
#             })
#             return record
#

from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _


class ResearchProject(models.Model):
    _name = "research.project"
    _description = "Research Project Model"

    # Fields
    name = fields.Char(string="Project Name", default="Project Name", required=True)
    start_date = fields.Date(default=lambda self: fields.Date.today())
    end_date = fields.Date(string="End Date")
    duration = fields.Integer(compute="_compute_duration", store=True, string="Duration (in days)")
    researcher_ids = fields.Many2many(
        "research.researcher",
        "research_project_researcher_rel",
        "project_id",
        "researcher_id",
        string="Researchers"
    )
    project_summary = fields.Text(
        string="Project Summary",
        help="Provide a brief description of the project’s goals, milestones, and outcomes."
    )
    status = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft', string="Status"
    )
    log_ids = fields.One2many("research.project.log", "project_id", string="Change Logs")

    # Compute duration
    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for research in self:
            if research.start_date and research.end_date:
                delta = research.end_date - research.start_date
                research.duration = delta.days
            else:
                research.duration = 30  # Default duration if end_date is not set

    # Validation for end_date
    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for research in self:
            if research.start_date and research.end_date:
                if research.end_date < research.start_date:
                    raise ValidationError("The end date cannot be earlier than the start date.")

    # Override write to add constraints and logging
    @api.model
    def write(self, vals):
        for record in self:
            # Prevent changes to end_date if the project is completed
            if record.status == 'completed' and 'end_date' in vals:
                if str(vals['end_date']) != str(record.end_date):
                    raise ValidationError("Cannot change the end date of a completed project.")

            # Log researcher changes
            if "researcher_ids" in vals:
                old_researchers = set(record.researcher_ids.ids)  # Existing researcher IDs
                new_researchers = old_researchers.copy()  # Start with the current researchers

                # Process the Many2many commands
                commands = vals["researcher_ids"]
                for command in commands:
                    if command[0] == 6:  # Replace all with IDs in the list
                        new_researchers = set(command[2])
                    elif command[0] == 4:  # Add a single researcher
                        new_researchers.add(command[1])
                    elif command[0] == 3:  # Remove a single researcher
                        new_researchers.discard(command[1])

                added = new_researchers - old_researchers
                removed = old_researchers - new_researchers

                changes = []
                if added:
                    added_names = self.env["research.researcher"].browse(added).mapped("name")
                    changes.append(f"Researchers added: {', '.join(added_names)}")
                if removed:
                    removed_names = self.env["research.researcher"].browse(removed).mapped("name")
                    changes.append(f"Researchers removed: {', '.join(removed_names)}")

                if changes:
                    self.env["research.project.log"].create({
                        "project_id": record.id,
                        "change_summary_assign": "\n".join(changes)
                    })

                # Update the researchers' profiles to reflect the change in the project
                for researcher_id in added:
                    self.env["research.researcher"].browse(researcher_id).write({
                        "project_ids": [(4, record.id)]  # Link the project to the researcher
                    })
                for researcher_id in removed:
                    self.env["research.researcher"].browse(researcher_id).write({
                        "project_ids": [(3, record.id)]  # Unlink the project from the researcher
                    })

        return super(ResearchProject, self).write(vals)

    # Log status changes
    def _log_status_change(self, new_status):
        self.env["research.project.log"].create({
            "project_id": self.id,
            "change_summary_status": f"Status updated to '{new_status}'."
        })

    # State change actions with validation
    def action_in_progress(self):
        self.ensure_one()
        if self.status in ['cancelled', 'completed']:
            raise UserError(_("Cannot move a cancelled or completed project to In Progress."))

        # Check if the status is already 'in_progress' before updating
        if self.status == "in_progress":
            raise UserError(_("This project is already marked as in progress."))

        # Update the status to 'in_progress' only if not already
        self.status = "in_progress"

        # Log the status change
        self._log_status_change("In Progress")
        return True

    def action_completed(self):
        self.ensure_one()
        if self.status in ['cancelled', 'completed']:
            raise UserError(_("Cannot mark a cancelled as Completed."))
        if self.status == "completed":
            raise UserError(_("This project is already marked as Completed."))
        self.status = "completed"
        self._log_status_change("Completed")
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.status == "completed":
            raise UserError(_("Cannot cancel a completed project."))
        if self.status == "cancelled":
            raise UserError(_("This project is already marked as in Cancelled."))
        self.status = "cancelled"
        self._log_status_change("Cancelled")
        return True






