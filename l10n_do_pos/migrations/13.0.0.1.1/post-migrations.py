import logging
from odoo import api, SUPERUSER_ID


_logger = logging.getLogger(__name__)


def migrate_fields(env):
    field_migrate = [
        ('pos_order', 'is_return_order', 'l10n_do_is_return_order'),
        ('pos_order', 'return_order_id', 'l10n_do_return_order_id'),
        ('pos_order', 'ncf', 'l10n_latam_document_number'),
        ('pos_order_line', 'line_qty_returned', 'l10n_do_line_qty_returned'),
        ('pos_order_line', 'original_line_id', 'l10n_do_original_line_id'),
        ('pos_config', 'default_partner_id', 'l10n_do_default_partner_id'),
        ('pos_config', 'order_loading_options', 'l10n_do_order_loading_options'),
        ('pos_config', 'number_of_days', 'l10n_do_number_of_days'),
        ('pos_config', 'credit_notes_number_of_days', 'l10n_do_credit_notes_number_of_days'),
    ]

    query1 = """
            UPDATE pos_order SET
            l10n_do_return_status = 'fully_returned'
            WHERE return_status = 'Fully-Returned' """
    query2 = """
            UPDATE pos_order SET
            l10n_do_return_status = 'partially_returned'
            WHERE return_status = 'Partially-Returned' """
    query3 = """
            UPDATE pos_order SET
            l10n_do_return_status = 'non_returnable'
            WHERE return_status = 'Non-Returnable' """

    _logger.info(
        """
        Migrating field:
        return_status ----> l10n_do_return_status"""
    )
    env.cr.execute(query1)
    env.cr.execute(query2)
    env.cr.execute(query3)


    for obj in field_migrate:

        query = """
        UPDATE %(table)s
        SET %(migrated)s = %(old_field)s
        """ % {
            'table': ''.join(obj[0:1]),
            'old_field': ''.join(obj[1:2]),
            'migrated': ''.join(obj[2:3])
        }

        _logger.info(
            """
            Migrating fields:
            %(old_field)s  ---->   %(migrated)s """
            % {
                'old_field': ''.join(obj[1:2]),
                'migrated': ''.join(obj[2:3])
            }
        )
        env.cr.execute(query)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    migrate_fields(env)
