{
    'name': "Eenadu Multi Delivary Order",
    'version': '16.0.0',
    'category': 'Sales',
    'summary': """ """,
    'description': """
        
    """,
    'depends': ['custom_purchase', 'sale', 'sale_management', 'sale_stock', 'stock', 'contacts', 'web', 'account', 'sales_team'],
    'website': "",
    'data': [
        'security/sales_team_group.xml',
        'security/ir.model.access.csv',
        'views/contact_inherit.xml',
        'views/res_users.xml',
        'views/duplicate_sale_order_line.xml',
        'views/sale_view.xml',
        'views/crm_team.xml',
        'views/agent_report.xml',
        'views/account_move.xml',
        'views/res_district.xml',
        'views/return_stock.xml',
        'views/menu_circulation.xml',
        'reports/paperformat.xml',
        'reports/delivery channel report.xml',
        'reports/report.xml',
        'views/agent_indent_webiste.xml',
        'views/agent_return_webiste.xml',
        'views/agent_deposit_website.xml',
    ],
    'assets': {
        'web.assets_backend' :[
            'sales_circulation/static/src/js/sales_circulation_dashboard.js',
            'sales_circulation/static/src/xml/sales_circulation_dashboard.xml',
       ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': -1,
}
