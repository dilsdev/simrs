# -*- coding: utf-8 -*-
# from odoo import http


# class RekamMedik(http.Controller):
#     @http.route('/rekam_medik/rekam_medik', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rekam_medik/rekam_medik/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rekam_medik.listing', {
#             'root': '/rekam_medik/rekam_medik',
#             'objects': http.request.env['rekam_medik.rekam_medik'].search([]),
#         })

#     @http.route('/rekam_medik/rekam_medik/objects/<model("rekam_medik.rekam_medik"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rekam_medik.object', {
#             'object': obj
#         })

