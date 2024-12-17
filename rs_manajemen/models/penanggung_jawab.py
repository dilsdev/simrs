# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Penanggung_jawab(models.Model):
    _name = 'cdn.penanggung_jawab'
    _description = 'Penanggung Jawab'

    kode = fields.Char(string='Kode', required=True)
    name = fields.Char(string='Penanggung Jawab', required=True)
    perusahaan_id = fields.Char(string='Nama Perusahaan')
    alamat= fields.Char(string='Alamat Asuransi')
    no_telfon= fields.Integer(string='No Telefon')
    attn= fields.Char(string='Attn')
    status = fields.Selection(string='Status', selection=[
        ('aktif', 'Aktif'), ('tidak_aktif', 'Tidak Aktif')
    ], required=True)

    