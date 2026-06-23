# -*- coding: utf-8 -*-
import time

import requests
from odoo import models
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"


    def _freshdesk_config(self):
        """ fetching domain and keys from settings and passes to the import or export functions"""

        config = (self.env["ir.config_parameter"].sudo())

        domain = config.get_param("freshdesk.domain")
        api_key = config.get_param("freshdesk.api_key")

        if not domain:
            raise UserError( "Configure Freshdesk Domain")
        if not api_key:
            raise UserError("Configure Freshdesk API Key")

        url = (f"https://{domain}"".freshdesk.com""/api/v2/contacts")
        return (url,api_key,)

    def export_contacts_to_freshdesk(self):
        """function to export contacts to freshdesk from odoo contacts"""

        url, api_key = self._freshdesk_config()
        exported = 0
        skipped = 0
        updated = 0

        partners = self.env["res.partner"].search([])
        for partner in partners:
            email = (partner.email or "").strip()
            if not email:
                skipped += 1
                continue
            payload = {
                "name": partner.name or email,
                "email": email,
                "phone": partner.phone or "",
            }
            try:
                search = requests.get(
                    url,
                    auth=(api_key, "X"),
                    params={"email": email},
                    timeout=30,
                )
                existing_id = None
                if search.status_code == 200:
                    contacts = search.json()
                    if contacts:
                        existing_id = contacts[0].get("id")
                if existing_id:
                    response = requests.put(
                        f"{url}/{existing_id}",
                        auth=(api_key, "X"),
                        json=payload,
                        timeout=30,
                    )
                    if response.status_code in [200, 201]:
                        updated += 1
                    else:
                        skipped += 1
                        time.sleep(0.5)
                else:
                    time.sleep(0.5)
                    response = requests.post(
                        url,
                        auth=(api_key, "X"),
                        json=payload,
                        timeout=30,
                    )
                    if response.status_code in [200, 201]:
                        exported += 1
                    else:
                        skipped += 1
                        time.sleep(0.5)
            except Exception as e:
                skipped += 1

    def import_contacts_from_freshdesk(self):
        """function for import contacts from freshdesk"""

        url, api_key = (self._freshdesk_config())
        created = 0
        updated = 0
        page = 1

        while True:

            response = (requests.get(f"{url}?page={page}",auth=(api_key,"X",),timeout=30,))
            if (response.status_code != 200):
                raise UserError(response.text)
            contacts = (response.json())
            if not contacts:
                break
            for contact in contacts:

                email = (
                    contact.get("email")or "").strip()
                if not email:
                    continue

                values = {
                    "name":contact.get("name")or "",
                    "email":email,
                    "phone":contact.get("phone")or "",
                }

                partner = (self.search([("email","=",email,)],limit=1,))

                if partner:
                    partner.write(values)
                    updated += 1
                else:
                    self.create( values)
                    created += 1
            page += 1
