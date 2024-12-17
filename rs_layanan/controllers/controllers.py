# -*- coding: utf-8 -*-
# from odoo import http


# class Layanan(http.Controller):
#     @http.route('/layanan/layanan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/layanan/layanan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('layanan.listing', {
#             'root': '/layanan/layanan',
#             'objects': http.request.env['layanan.layanan'].search([]),
#         })

#     @http.route('/layanan/layanan/objects/<model("layanan.layanan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('layanan.object', {
#             'object': obj
#         })

