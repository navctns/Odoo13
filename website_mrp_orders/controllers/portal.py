import binascii

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression






# class PortalMrp(http.Controller):
class PortalMrp(CustomerPortal):
    orders_page = '/my/orders'

    def _get_current_user(self):
        return request.env.user

    @http.route(['/my/mrporders', '/my/mrporders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_mrp_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        # values = self._prepare_portal_layout_values()
        user = self._get_current_user()
        orders = request.env['mrp.production'].search([('partner_id', '=', user.id)])
        return request.render("website_mrp_orders.portal_my_mrp_orders",{'orders':orders.sudo()})
            # values = self._prepare_portal_layout_values()
            # partner = request.env.user.partner_id
            # SaleOrder = request.env['mrp.production']
            #
            # domain = [
            #     ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            #     ('state', 'in', ['sent', 'cancel'])
            # ]
            #
            # searchbar_sortings = {
            #     'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            #     'name': {'label': _('Reference'), 'order': 'name'},
            #     'stage': {'label': _('Stage'), 'order': 'state'},
            # }
            #
            # # default sortby order
            # if not sortby:
            #     sortby = 'date'
            # sort_order = searchbar_sortings[sortby]['order']
            #
            # archive_groups = self._get_archive_groups('sale.order', domain)
            # if date_begin and date_end:
            #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
            #
            # # count for pager
            # quotation_count = SaleOrder.search_count(domain)
            # # make pager
            # pager = portal_pager(
            #     url="/my/mrporders",
            #     url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            #     total=quotation_count,
            #     page=page,
            #     step=self._items_per_page
            # )
            # # search the count to display, according to the pager data
            # quotations = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
            # request.session['my_quotations_history'] = quotations.ids[:100]
            #
            # values.update({
            #     'date': date_begin,
            #     'quotations': quotations.sudo(),
            #     'page_name': 'quote',
            #     'pager': pager,
            #     'archive_groups': archive_groups,
            #     'default_url': '/my/quotes',
            #     'searchbar_sortings': searchbar_sortings,
            #     'sortby': sortby,
            # })
            # return request.render("sale.portal_my_mrp_orders")
    @http.route(['/my/mrporders/cancel', '/my/mrporders/page/<int:page>/cancel'], type='http', auth="user", website=True)
    def portal_my_mrp_orders_cancel(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        # values = self._prepare_portal_layout_values()
        orders = request.env['mrp.production'].action_cancel()
        # user = self._get_current_user()
        # orders = request.env['mrp.production'].search([('partner_id', '=', user.id)])
        # return request.render("website_mrp_orders.portal_my_mrp_orders",{'orders':orders.sudo()})
        return request.redirect(self.orders_page)