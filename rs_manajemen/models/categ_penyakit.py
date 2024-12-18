# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Penyakit(models.Model):
    _name = 'cdn.penyakit'
    _description = 'Kategori Penyakit'
    _sql_constraints = [
        ('unique_penyakit_id', 'UNIQUE(penyakit_id)', 'Kode Penyakit harus unik!'),
    ]


    penyakit_id = fields.Char(string='Kode Penyakit', required=True, help="Masukkan kode 3 angka (contoh: A01).")
    name = fields.Char(string='Nama Penyakit', required=True)
    ciri = fields.Char(string="Ciri Umum", help="Ciri umum dari penyakit ini.")

    @api.constrains('penyakit_id')
    def _check_penyakit_id(self):
        for record in self:
            if not re.match(r'^\d{3}$', record.penyakit_id):
                raise ValidationError("Kode Penyakit harus terdiri dari 3 angka (contoh: 001, 123).")
