from odoo import api, models, fields
import json
import pprint


def filter_values(values):
    """Remove non-scalar and no-jsonable elements of a dictionary."""
    res = dict()
    f_filter = lambda v: isinstance(v, str) or isinstance(v, int) or isinstance(v, float) or isinstance(v, bool)
    for k,v in values.items():
        if f_filter(v):
            res[k] = v
    return res

class AuditTrackingMixin(models.AbstractModel):
    _name = 'audit.tracking.mixin'
    _description = 'Change Tracking Mixin'
    
    audit_tracking_ids = fields.One2many('audit.value', string='Past Changes', compute='_compute_audit_values')
    
    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        changes = {
            'post': json.dumps(filter_values(vals), skipkeys=True),
            'change_type': 'create',
            'res_model': self._name,
            'res_id': res.id,
        }
        self.env['audit.value'].create(changes)
        return res
    
    def write(self, vals):
        pre_values = self.read(vals.keys())
        res = super().write(vals)
        changes = {
            'post': json.dumps(filter_values(vals)),
            'change_type': 'write',
            'res_model': self._name,
        }
        for record in self:
            vals = filter(lambda v: v['id'] == record.id, pre_values)
            record_vals = list(vals)[0]
            changes.update({
                'res_id': record.id,
                'pre': json.dumps(filter_values(record_vals))
            })
            self.env['audit.value'].create(changes)
        return res

    def unlink(self):
        changes = {
            'change_type': 'unlink',
            'res_model': self._name,
        }
        pre_values = self.read([])
        for res_id in self.ids:
            vals = filter(lambda v: v['id'] == res_id, pre_values)
            record_vals = list(vals)[0]
            changes.update({
                'res_id': res_id,
                'pre': json.dumps(filter_values(record_vals))
            })            
            self.env['audit.value'].create(changes)
        return super().unlink()

    def _compute_audit_values(self):
        for record in self:
            trackings = self.env['audit.value'].search([('res_model', '=', self._name), ('res_id', '=', record.id)])
            record.audit_tracking_ids = trackings