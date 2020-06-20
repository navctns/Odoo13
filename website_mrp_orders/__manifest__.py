

{
    'name': 'website_mrp_orders',
    'version': '13.0.1.0.0',
    'summary': """This Module Allows Customer to Download Documents
    That Are Attached to the Products From Website""",
    'description': 'This Module allows customer to download documents '
                   'that are attached to the products from website',
    'category': 'Website',
    'author': 'nav',
    'company': 'nav',
    'maintainer': 'nav',
    'website': "https://www.sample.com",
    'depends': ['website_sale','mrp','portal','website_partner'],
    'data': ['views/mrp_add_partner.xml',
             'views/portal_myhome_inherit.xml',
            # 'views/button_buy_now.xml',
             ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}