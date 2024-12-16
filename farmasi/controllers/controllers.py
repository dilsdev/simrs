# -*- coding: utf-8 -*-
# from odoo import http


# class Farmasi(http.Controller):
#     @http.route('/farmasi/farmasi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/farmasi/farmasi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('farmasi.listing', {
#             'root': '/farmasi/farmasi',
#             'objects': http.request.env['farmasi.farmasi'].search([]),
#         })

#     @http.route('/farmasi/farmasi/objects/<model("farmasi.farmasi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('farmasi.object', {
#             'object': obj
#         })

