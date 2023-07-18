# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Eenadu Reta',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Custom Sales',
    'description': 'Sales Enhancement',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': [
        'sale', 'stock', 'sale_stock', 'sales_team', 'sales_circulation', 'web', 'web_tour','contacts',
    ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/scheduling_line_update_wizard_views.xml',
        'wizard/create_payment_views.xml',
        'views/sale_order_views.xml',
        'views/sales_custom.xml',
        'views/newspaper_page_details_views.xml',
        'views/advertisement_position_views.xml',
        'views/views.xml',
        'views/advertisement_position_views.xml',
        'views/sale_document_type_views.xml',
        'views/account_payment_views.xml',
        'views/agent_commission_website.xml',
        'views/employee_incentive.xml',
        'views/cio_portal_form.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'eenadu_reta/static/src/js/reta_dashboard.js',
            'eenadu_reta/static/src/xml/reta_dashboard.xml',
            # 'eenadu_reta/static/src/xml/cio_portal_form.xml',
            'eenadu_reta/static/src/css/stylesheet.css',
            # 'eenadu_reta/static/src/css/boostrap.css',
        ],
        'web.assets_frontend': [
            'eenadu_reta/static/src/js/reta_portal.js',
            'eenadu_reta/static/src/css/stylesheet.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
