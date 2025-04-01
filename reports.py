import base64
import io
from odoo import api,models, fields
from odoo.exceptions import UserError
# from xlsxwriter.workbook import Workbook
from odoo.tools.misc import xlsxwriter

class ResearchReporting(models.TransientModel):
    """
        A transient model for generating research project reports.

        This wizard allows users to generate reports for research projects within a specified date range.
        Users can choose between two report formats: PDF and Excel.
    """
    _name = 'research.reporting'
    _description = 'Research Reporting'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    report_format = fields.Selection([('pdf', 'PDF'), ('excel', 'Excel')], string='Report Format', required=True)

    def validate_dates(self):
        """Ensure start date is before or equal to end date."""
        if self.start_date > self.end_date:
            raise UserError("Start date cannot be after End date.")

    formatted_start_date = fields.Char(compute='_compute_formatted_dates', store=False)
    formatted_end_date = fields.Char(compute='_compute_formatted_dates', store=False)

    @api.depends('start_date', 'end_date')
    def _compute_formatted_dates(self):
        for record in self:
            record.formatted_start_date = record.start_date.strftime('%d/%m/%Y') if record.start_date else ''
            record.formatted_end_date = record.end_date.strftime('%d/%m/%Y') if record.end_date else ''

    def generate_report(self):
        """Generate the report based on the date range and format."""
        self.validate_dates()

        # Fetching the research projects within the date range
        research_projects = self.env['research.project'].search([
            ('start_date', '>=', self.start_date),
            ('end_date', '<=', self.end_date)
        ])

        # Generate the report based on the selected format
        if self.report_format == 'pdf':
            return self.generate_pdf_report(research_projects)
        elif self.report_format == 'excel':
            return self.generate_excel_report(research_projects)

    # PDF Report
    def generate_pdf_report(self, research_projects):
        """Generate PDF report logic."""
        if not research_projects:
            raise UserError("No research projects found within the selected date range.")

        # Ensure start_date and end_date are passed to the report
        start_date = self.formatted_start_date
        end_date = self.formatted_end_date

        # Aggregate start and end dates for the selected range
        if not start_date or not end_date:
            start_date = min(research_projects.mapped('start_date'))
            end_date = max(research_projects.mapped('end_date'))

        # Determine the report type based on whether a date range was provided
        report_type = "date_range" if start_date and end_date else "single_project"
        # print(report_type)

        # Prepare report values
        values = {
            'docs': research_projects,
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Generate the PDF content
        report_service = self.env["ir.actions.report"]
        report_name = "research_management.report_research_project"

        pdf_content, _ = report_service._render_qweb_pdf(
            report_name,
            res_ids=research_projects.ids,
            data=values)

        pdf_filename = "Research_Project_Report.pdf"

        # Create an attachment for the generated PDF
        attachment = self.env['ir.attachment'].create({
            'name': pdf_filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
            'res_model': 'research.reporting',  # Model linked to the wizard
            'res_id': self.id,
        })

        # Return a URL pointing to the generated attachment
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }


    #Excel report
    def generate_excel_report(self, research_projects):
        """Generate Excel report logic."""
        if not research_projects:
            raise UserError("No research projects found within the selected date range.")

        # Create an Excel file in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Research Projects")

        # Define formatting styles
        title_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 14})
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D3D3D3'})
        cell_format = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True})  # Added text wrap for Project Summary

        # Merge first row across 7 columns and write title
        title = f"Research Projects – {self.formatted_start_date} to {self.formatted_end_date}"
        sheet.merge_range(0, 0, 0, 6, title, title_format)  # Adjusted to span 7 columns

        # Define column headers (including "Project Summary")
        headers = ["Project Name", "Start Date", "End Date", "Project Summary", "Duration", "Status",
                   "Assigned Researchers","Sequence Number"]

        # Set column widths for better readability
        column_widths = [30, 15, 15, 40, 10, 15, 40,15]  # Adjust widths, with added space for "Project Summary"
        for col, (header, width) in enumerate(zip(headers, column_widths)):
            sheet.set_column(col, col, width)
            sheet.write(1, col, header, header_format)

        # Populate the sheet with data
        for row, project in enumerate(research_projects, start=2):  # Start from row 2
            researchers = ", ".join(project.researcher_ids.mapped("name")) if project.researcher_ids else "none"

            sheet.write(row, 0, project.name, cell_format)
            sheet.write(row, 1, str(project.formatted_start_date) if project.formatted_start_date else " ", cell_format)
            sheet.write(row, 2, str(project.formatted_end_date) if project.formatted_end_date else " ", cell_format)
            sheet.write(row, 3, project.project_summary if project.project_summary else "N/A",
                        cell_format)
            sheet.write(row, 4, project.duration if project.duration else "0", cell_format)
            sheet.write(row, 5, project.status if project.status else "N/A", cell_format)
            sheet.write(row, 6, researchers, cell_format)
            sheet.write(row, 7,project.sequence_number,cell_format)

        # Close the workbook
        workbook.close()
        output.seek(0)

        # Create an attachment for the Excel file
        attachment = self.env['ir.attachment'].create({
            'name': f"Research_Project_Report_{fields.Date.today().strftime('%Y-%m-%d')}.xlsx",
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        output.close()

        # Return the download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
