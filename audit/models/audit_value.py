from odoo import api, models, fields


class AuditValue(models.Model):
    _name = 'audit.value'
    _description = 'Audit Tracking Values'
    
    name = fields.Char(compute='_compute_name', store=True)
    res_model = fields.Char(string='Model Name', required=True)
    res_id = fields.Integer(string='Record ID', required=True)
    pre = fields.Text(string='Values before change')
    post = fields.Text(string='Values after change')
    change_type = fields.Selection([('create', 'Creation'), ('write', 'Modification'), ('unlink', 'Deletion')], string='Type of change', required=True)
    create_date = fields.Datetime(string='Date of changes')
    create_uid = fields.Many2one('res.users', string='Author of the changes')

    @api.depends('res_model', 'res_id', 'change_type', 'create_uid')
    def _compute_name(self):
        for record in self:
            record.name = '%s - %s (%s,%s)' % (record.change_type, record.create_uid.name, record.res_model, record.res_id)