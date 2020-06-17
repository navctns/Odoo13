# # -*- coding: utf-8 -*-
# {
#     'name': "website_buynow_button",
#     'category': 'Website/Website',
#     'summary': """
#         Short (1 phrase/line) summary of the module's purpose, used as
#         subtitle on modules listing or apps.openerp.com""",
#
#     'description': """
#         Long description of module's purpose
#     """,
#
#     'author': "My Company",
#     'website': "http://www.yourcompany.com",
#
#     # Categories can be used to filter modules in modules listing
#     # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
#     # for the full list
#     # 'category': 'Uncategorized',
#     'version': '0.1',
#
#     # any module necessary for this one to work correctly
#     'depends': ['base','point_of_sale','sale','product','website_sale'],
#
#     # always loaded
#     'data': [
#         # 'security/ir.model.access.csv',
#         # 'views/views.xml',
#         # 'views/templates.xml',
#         # 'views/product_grade.xml',
#         'templates.xml',
#         'views/button_buy_now.xml',
#     ],
#     # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
#
#     'qweb': [
#         # 'static/src/xml/discount_templates.xml',
#         # 'static/src/xml/product_grade_on_ticket.xml',
#         # 'static/src/xml/order_reciept_inherit.xml',
#         # 'static/src/xml/extend_reciept_fields.xml',
#         # 'static/src/xml/buynow_button.xml',
#
#     ],
# }

{
    'name': 'Buy Now Button on Website',
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
    'depends': ['website_sale'],
    'data': ['views/templates.xml',
            # 'views/button_buy_now.xml',
             ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}