# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Kategori_perawatan(models.Model):
    _name = 'cdn.kategori_perawatan'
    _description = 'Kategori Perawatan'

    kode_id = fields.Char(string='Kode Kategori Rawatan', required=True, copy=False, readonly=True, default='CP/20XX/XXX')
    name= fields.Char(string='Nama', required=True)

    @api.model
    def create(self, vals):
        if vals.get('kode_id', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record = self.search([('kode_id', 'like', f'CP/{current_year}/%')], order='id desc', limit=1)

            if last_record:
                last_id = last_record.kode_id
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1

            vals['kode_id'] = f'CP/{current_year}/{new_number:03d}'
        return super(Kategori_perawatan, self).create(vals)
