from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import create_index


class SchoolGroup(models.Model):
    _name = "school.group"
    _inherit = ["mail.thread"]
    _description = "Group"

    def _default_supervisor_id(self):
        return self.env.user.partner_id

    name = fields.Char()
    student_ids = fields.One2many(
        "res.partner",
        "school_group_id",
        string="Students",
        domain=[("student", "=", True)],
    )
    student_count = fields.Integer(
        string="Number of Students",
        compute="_compute_student_count",
        store=True,
    )
    supervisor_id = fields.Many2one(
        "res.partner",
        string="Supervisor",
        required=True,
        domain=[("teacher", "=", True)],
        default=_default_supervisor_id,
    )

    _sql_constraints = [
        ("uniq_name", "unique(name)", "School Group names must be unique")
    ]

    @api.depends("student_ids")
    def _compute_student_count(self):
        # TODO: improve perf and remove naive implementation
        for group in self:
            group.student_count = len(group.student_ids)

    def _search_student_count(self, operator, value):
        # map incoming operator with a comparison function
        operators = {
            "=": lambda e: e == value,
            "!=": lambda e: e != value,
            ">": lambda e: e > value,
            ">=": lambda e: e >= value,
            "<": lambda e: e <= value,
            "<=": lambda e: e <= value,
        }
        fun_op = operators[operator]
        # get the number of students grouped by group
        student_per_group = self.env["res.partner"].read_group(
            [("student", "=", True), ("school_group_id", "!=", False)],
            groupby=["school_group_id"],
            fields=["id"],
        )
        # filter the sudent groups with the comparison function
        matching_groups = filter(
            lambda c: fun_op(c["school_group_id_count"]), student_per_group
        )
        # get the ids of the groups from the dict structure
        matching_group_ids = list(
            map(lambda c: c["school_group_id"][0], matching_groups)
        )
        return [("id", "in", matching_group_ids)]
