# -*- coding: utf-8 -*-
{
    "name": "Freshdesk Contact Export",
    'version': '19.0.1.0.0',
    'depends': ["contacts"],
    'summary': 'freshdesk contact import to odoo contacts and export contacts to freshdesk',
    'category': 'Real Estate',
    'data': [
        "views/res_config_settings_view.xml",
    ],
    'application': True,
    'installable': True,
    'sequence': 1,
}