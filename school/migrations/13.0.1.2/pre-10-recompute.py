from openupgradelib import openupgrade
from odoo.api import Environment


@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    import pudb; pu.db
    env = Environment(cr, 1, {})
    cr.execute('ALTER TABLE school_group ADD COLUMN student_count int4')
    cr.execute('ALTER TABLE school_group ADD COLUMN some_field float')
    cr.execute("""
        WITH students AS (
            SELECT school_group_id as group,count(*) as count
            FROM res_partner
            WHERE school_group_id IS NOT NULL
            GROUP BY school_group_id
        )
        UPDATE school_group
        SET student_count = students.count
        FROM students
        WHERE students.group=school_group.id
    """)