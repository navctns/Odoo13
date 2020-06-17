# # -*- coding: utf-8 -*-
from odoo import http
#
#
# # class PosAddDiscount(http.Controller):
# #     @http.route('/pos_add_discount/pos_add_discount/', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"
#
# #     @http.route('/pos_add_discount/pos_add_discount/objects/', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('pos_add_discount.listing', {
# #             'root': '/pos_add_discount/pos_add_discount',
# #             'objects': http.request.env['pos_add_discount.pos_add_discount'].search([]),
# #         })
#
# #     @http.route('/pos_add_discount/pos_add_discount/objects/<model("pos_add_discount.pos_add_discount"):obj>/', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('pos_add_discount.object', {
# #             'object': obj
# #         })
#
from odoo.addons.website_sale.controllers.main import WebsiteSale
# class BuyNowButton(http.Controller):
    # @http.route('/shop/', auth='public')
# class BuyNowButton(http.Controller):
    # ['/shop/product/<model("product.template"):product>']

#not necessary when value is not passed
# class WebsiteSale(WebsiteSale):
#
#     @http.route('/shop/', type='http', auth="public", website=True)
#     def index(self, **kw):
#         # return http.request.render('website_button_buyNow.products_item_buynow1')
#         return http.request.render('website_sale.products_item')
        # website_sale.products_item
#         #                            {
#         #     'root': '/website_button_buyNow/views',
#         # })
#         #                            {
#         #     'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
#         # })
#
