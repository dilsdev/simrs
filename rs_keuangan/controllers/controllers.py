# -*- coding: utf-8 -*-
# from odoo import http


# class Keuangan(http.Controller):
#     @http.route('/keuangan/keuangan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/keuangan/keuangan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('keuangan.listing', {
#             'root': '/keuangan/keuangan',
#             'objects': http.request.env['keuangan.keuangan'].search([]),
#         })

#     @http.route('/keuangan/keuangan/objects/<model("keuangan.keuangan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('keuangan.object', {
#             'object': obj
#         })

