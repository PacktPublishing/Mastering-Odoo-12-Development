from odoo import models


class SchoolGroup(models.Model):
    _name = 'school.group'
    _inherit = ['school.group', 'mail.thread']
