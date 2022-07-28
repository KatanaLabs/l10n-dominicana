from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.update_module_names(env.cr, [('ncf_pos', 'l10n_do_pos')], merge_modules=True)
