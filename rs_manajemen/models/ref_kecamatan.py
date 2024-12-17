#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

class Ref_kecamatan(models.Model):

    _name               = "cdn.ref_kecamatan"
    _description        = "Tabel Data Ref Kecamatan"

    name                = fields.Char( required=True, string="Nama Kecamatan",  help="")
    keterangan          = fields.Char( string="Keterangan",  help="")


    kota_id             = fields.Many2one(comodel_name="cdn.ref_kota",  string="Kota",  help="")
    desa_ids            = fields.One2many(comodel_name="cdn.ref_desa",  inverse_name="kecamatan_id",  string="Desa",  help="")
