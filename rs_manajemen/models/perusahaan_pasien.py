# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Perusahaan_pasien(models.Model):
    _name = 'cdn.perusahaan_pasien'
    _description = 'Perusahaan pasien'

    kode_perusahaan = fields.Char(string='Kode Perusahaan', required=True)
    name= fields.Char(string='Nama Perusahaan', required=True)
    alamat= fields.Char(string='Alamat Perusahaan', required=True)
    kota= fields.Many2one('cdn.ref_kota', string='Kota', required=True)
    no_telfon= fields.Integer(string='No Telefon')

    