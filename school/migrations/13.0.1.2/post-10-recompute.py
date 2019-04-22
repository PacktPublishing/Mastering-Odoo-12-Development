from openupgradelib import openupgrade

from odoo.api import Environment

def migrate(cr, version):
    import pudb; pu.db
    cr.execute('SELECT id FROM school_group WHERE some_field IS NULL')
    recompute_ids = list(map(lambda e: e[0], cr.fetchall()))
    with Environment.manage():
        env = Environment(cr, 1, {})
        records = env['school.group'].browse(recompute_ids)
        #records._recompute_some_field()