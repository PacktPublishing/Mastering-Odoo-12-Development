from datetime import date, timedelta

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    student = fields.Boolean()
    teacher = fields.Boolean()
    school_group_id = fields.Many2one(
        "school.group", string="School Group", auto_join=True
    )
    supervisor_id = fields.Many2one(
        "res.partner",
        related="school_group_id.supervisor_id",
        readonly=True,
        store=True,
    )
    option_ids = fields.Many2many(
        "school.option",
        relation="student_option_rel",
        column1="student_id",
        column2="option_id",
        string="Options",
    )
    birthdate = fields.Date(string="Date of Birth", groups="school.group_manager")
    inscription_date = fields.Date(
        string="Inscription Date", default=fields.Date.context_today
    )
    member_for = fields.Integer(
        string="Member for (days)",
        compute="_compute_member_for",
        inverse="_inverse_member_for",
    )
    student_type = fields.Selection(
        [("free", "Free"), ("full", "Full")], default="full"
    )

    @api.depends("inscription_date")
    def _compute_member_for(self):
        for student in self:
            delta = date.today() - student.inscription_date
            student.member_for = delta.days

    def _inverse_member_for(self):
        for student in self:
            student.inscription_date = date.today() - timedelta(days=student.member_for)

    @api.onchange("member_for")
    def _onchange_member_for(self):
        self._inverse_member_for()
