from openupgradelib import openupgrade

@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    # low hanging fruit first in a single query:
    # teachers that are also students
    cr.execute("""
        UPDATE res_partner
        SET student_type = 'employee'
        WHERE teacher = true AND
              student = true
    """)
    # then we check the security groups
    # let's get the security group id first
    cr.execute("SELECT res_id FROM ir_model_data WHERE module='school' AND name='group_user'")
    group_id = cr.fetchone()[0]
    # then we update all members of this group
    cr.execute("""
        WITH employees AS (
            SELECT uid AS id
            FROM res_groups_users_rel
            WHERE gid=%s
        )
        UPDATE res_partner
        SET student_type = 'employee'
        FROM employees
        WHERE employees.id = res_partner.id AND
              res_partner.student = true
    """, (group_id,))
