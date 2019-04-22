from openupgradelib import openupgrade
from odoo.api import Environment


@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    cr.execute('ALTER TABLE school_group ADD COLUMN student_count int4')
