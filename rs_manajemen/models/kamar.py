# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Kamar(models.Model):
    _name = 'cdn.kamar'
    _description = 'Kamar'

    kamar_id = fields.Char(string='Nomor Kamar', required=True, copy=False, readonly=True, default='KMR/20XX/XXX')
    bangsal_id = fields.Many2one('cdn.bangsal', string='Nama Bangsal', required=True)
    tarif = fields.Integer(string='Tarif Kamar', required=True)
    status = fields.Selection(string='Status', selection=[
        ('isi', 'ISI'), ('kosong', 'KOSONG'), 
        ('dibersihkan', 'DIBERSIHKAN'), ('dibooking', 'DIBOOKING')
    ], required=True)
    kelas = fields.Selection(string='Kelas', selection=[
        ('kelas_1', 'Kelas 1'), ('kelas_2', 'Kelas 2'), 
        ('kelas_3', 'Kelas 3'), ('kelas_utama', 'Kelas utama'),
        ('kelas_vip', 'Kelas VIP'), ('kelas_vvip', 'Kelas VVIP')
    ], required=True)
    status_data = fields.Selection(string='Status Data', selection=[
        ('aktif', 'Aktif'), ('tidak_aktif', 'Tidak Aktif')
    ], required=True)


    @api.model
    def create(self, vals):
        if vals.get('kamar_id', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record = self.search([('kamar_id', 'like', f'KMR/{current_year}/%')], order='id desc', limit=1)

            if last_record:
                last_id = last_record.kamar_id
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1

            vals['kamar_id'] = f'KMR/{current_year}/{new_number:03d}'
        return super(Kamar, self).create(vals)