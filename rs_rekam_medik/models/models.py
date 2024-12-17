# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rekam_medik(models.Model):
#     _name = 'rekam_medik.rekam_medik'
#     _description = 'rekam_medik.rekam_medik'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

