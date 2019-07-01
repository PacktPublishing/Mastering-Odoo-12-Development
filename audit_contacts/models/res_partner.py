from odoo import models


class ResPartner(models.Model):
    _inherit = ['res.partner', 'audit.tracking.mixin']
    _name = 'res.partner'