# -*- coding: utf-8 -*-
# from odoo import http


# class Laporan(http.Controller):
#     @http.route('/laporan/laporan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/laporan/laporan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('laporan.listing', {
#             'root': '/laporan/laporan',
#             'objects': http.request.env['laporan.laporan'].search([]),
#         })

#     @http.route('/laporan/laporan/objects/<model("laporan.laporan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('laporan.object', {
#             'object': obj
#         })

