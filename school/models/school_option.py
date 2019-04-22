from odoo import models, fields


class SchoolOption(models.Model):
    _name = "school.option"
    _description = "School Option"

    name = fields.Char(required=True)
    student_ids = fields.Many2many(
        "res.partner",
        relation="student_option_rel",
        column1="option_id",
        column2="student_id",
        domain=[("student", "=", True)],
        string="Students",
    )
