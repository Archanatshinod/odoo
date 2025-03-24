# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderApproval(http.Controller):
#     @http.route('/sale_order_approval/sale_order_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_approval/sale_order_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_approval.listing', {
#             'root': '/sale_order_approval/sale_order_approval',
#             'objects': http.request.env['sale_order_approval.sale_order_approval'].search([]),
#         })

#     @http.route('/sale_order_approval/sale_order_approval/objects/<model("sale_order_approval.sale_order_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_approval.object', {
#             'object': obj
#         })

