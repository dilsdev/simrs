# -*- coding: utf-8 -*-
# from odoo import http


# class Anjungan(http.Controller):
#     @http.route('/anjungan/anjungan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anjungan/anjungan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('anjungan.listing', {
#             'root': '/anjungan/anjungan',
#             'objects': http.request.env['anjungan.anjungan'].search([]),
#         })

#     @http.route('/anjungan/anjungan/objects/<model("anjungan.anjungan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anjungan.object', {
#             'object': obj
#         })

