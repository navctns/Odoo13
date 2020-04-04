# -*- coding: utf-8 -*-
# from odoo import http


# class NewModuleNav(http.Controller):
#     @http.route('/new_module_nav/new_module_nav/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_module_nav/new_module_nav/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_module_nav.listing', {
#             'root': '/new_module_nav/new_module_nav',
#             'objects': http.request.env['new_module_nav.new_module_nav'].search([]),
#         })

#     @http.route('/new_module_nav/new_module_nav/objects/<model("new_module_nav.new_module_nav"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_module_nav.object', {
#             'object': obj
#         })
