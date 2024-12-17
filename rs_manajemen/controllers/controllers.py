# -*- coding: utf-8 -*-
# from odoo import http


# class Manajemen(http.Controller):
#     @http.route('/manajemen/manajemen', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manajemen/manajemen/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manajemen.listing', {
#             'root': '/manajemen/manajemen',
#             'objects': http.request.env['manajemen.manajemen'].search([]),
#         })

#     @http.route('/manajemen/manajemen/objects/<model("manajemen.manajemen"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manajemen.object', {
#             'object': obj
#         })

