from openupgradelib import openupgrade


@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    openupgrade.update_module_names(cr, [('mail_school', 'school')], merge_modules=True)
