# -*- coding: utf-8 -*-

{
    'name': 'CRM Call Logs - Odoo',
    'version': '16.0.1.0.1',
    'category': 'Localization',
    'summary': 'Connect call to customer and get call details from API and store',
    'description': 'Connect call to customer and get call details from API and store',
    'website': 'https://www.primeminds.co',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'depends': ['crm', 'base'],
    'support': 'https://www.primeminds.co',
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_menu_views.xml',
        'views/crm_api_view.xml',
        'views/access_token.xml',
        'views/hr_employee.xml',
        'views/menu_item.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
