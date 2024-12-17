# -*- coding: utf-8 -*-
# from odoo import http


# class Bridging(http.Controller):
#     @http.route('/bridging/bridging', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bridging/bridging/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bridging.listing', {
#             'root': '/bridging/bridging',
#             'objects': http.request.env['bridging.bridging'].search([]),
#         })

#     @http.route('/bridging/bridging/objects/<model("bridging.bridging"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bridging.object', {
#             'object': obj
#         })

