# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    freshdesk_domain = fields.Char(
        string="Freshdesk Domain",
        config_parameter="freshdesk.domain",
    )

    freshdesk_api_key = fields.Char(
        string="Freshdesk API Key",
        config_parameter="freshdesk.api_key",
    )

    def action_export_contacts(self):
        """ button action to export contacts this action will call the export function"""

        self.env["res.partner"].export_contacts_to_freshdesk()

    def action_import_contacts(self):
        """ button action to import contacts this action will call the import function"""

        self.env["res.partner"].import_contacts_from_freshdesk()