from odoo import  api,fields, models
from odoo.exceptions import ValidationError

class ResearchProject(models.Model):
    """
        The `ResearchProject` model is used to track information related to a research project. It includes
        fields such as the project name, start date, end date, project summary, and the researchers involved.
        The model also manages the status of the project, allowing transitions between 'Draft', 'In Progress',
        'Completed', and 'Cancelled' states. It includes methods to compute the project's duration, validate
        the dates, and post notifications when the project status changes.
    """
    _name = "research.project"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Research Project Model"

    # Fields
    name = fields.Char(string="Project Name", required=True, tracking=True)
    start_date = fields.Date(default=lambda self: fields.Date.today(),required=True)
    end_date = fields.Date(string="End Date",required=True)
    duration = fields.Integer(compute="_compute_duration", store=True, string="Duration (in days)", default=30)
    researcher_ids = fields.Many2many(
        "research.researcher",
        "research_project_researcher_rel",
        "project_id",
        "researcher_id",
        string="Researchers",
        tracking=True,required=True

    )
    is_archived = fields.Boolean('Is Archived', default=False)
    project_summary = fields.Text(
        string="Project Summary",
        help="Provide a brief description of the project’s goals, milestones, and outcomes.",
        required=True
    )
    status = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft',
        string="Status",
        tracking=True,
    )

    # Compute duration
    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        """
            The _compute_duration method computes the duration between the start and end dates for a research record.
            This function is triggered when either the `start_date` or `end_date` fields are modified.
            It calculates the number of days between the `start_date` and `end_date` and stores the result
            in the `duration` field. If either of the dates is missing, the function assigns a default
            duration of 30 days.
            The computed duration is stored in the `duration` field.
        """

        for research in self:
            if research.start_date and research.end_date:
                delta = research.end_date - research.start_date
                research.duration = delta.days
            else:
                research.duration = 30  # Default duration set to 30 days if not computed




    # Validation for end_date
    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        """
            The _check_dates method validates the relationship between the start and end dates for a research record.
            This function is triggered when either the `start_date` or `end_date` fields are modified.
            It checks that the `end_date` is not earlier than the `start_date`. If the `end_date` is found
            to be earlier than the `start_date`, a `ValidationError` is raised with an appropriate error message.
        """

        for research in self:
            if research.start_date and research.end_date and research.end_date < research.start_date:
                raise ValidationError("The end date cannot be earlier than the start date.")


    # methods for status updates post messages
    def action_in_progress(self):
        """
           action_in_progress method updates the project status to 'In Progress' and posts a notification message.
           This function sets the `status` field of the current project to 'in_progress'. Additionally,
           it posts a message in the project's message wall notifying that the project status has been updated
           to 'In Progress'. The message is posted with the appropriate note subtype.
        """
        self.status = 'in_progress'
        self.message_post(
            body="Project status updated to In Progress.",
            subtype_id=self.env.ref('mail.mt_note').id,
        )

    def action_completed(self):
        """
          action_completed method updates the project status to 'Completed' and posts a notification message.
          This function sets the `status` field of the current project to 'completed'. Additionally,
          it posts a message in the project's message wall notifying that the project status has been updated
          to 'Completed'. The message is posted with the appropriate note subtype.
        """
        self.status = 'completed'
        self.message_post(
            body="Project status updated to Completed.",
            subtype_id=self.env.ref('mail.mt_note').id,
        )

    def action_cancel(self):
        """
             action_cancel method updates the project status to 'Cancelled' and posts a notification message.
             This function sets the `status` field of the current project to 'cancelled'. Additionally,
             it posts a message in the project's message wall notifying that the project status has been updated
             to 'Cancelled'. The message is posted with the appropriate note subtype.
        """

        self.status = 'cancelled'
        self.message_post(
            body="Project status updated to Cancelled.",
            subtype_id=self.env.ref('mail.mt_note').id,
        )




