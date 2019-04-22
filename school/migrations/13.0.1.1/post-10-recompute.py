from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute('SELECT id FROM school_group WHERE student_count IS NULL')
    recompute_ids = list(map(lambda e: e[0], env.cr.fetchall()))
    groups = env['school.group'].browse(recompute_ids)
    for batch in openupgrade.chunked(groups):
        batch._compute_student_count()
