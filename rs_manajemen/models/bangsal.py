# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Bangsal(models.Model):
    _name = 'cdn.bangsal'
    _description = 'Bangsal'

    bangsal_id = fields.Char(string='Nomor Bangsal', required=True, copy=False, readonly=True, default='BSL/20XX/XXX')
    name = fields.Char(string='Nama Bangsal', required=True)
    status = fields.Selection(string='Status', selection=[
        ('aktif', 'Aktif'), ('tidak_aktif', 'Tidak Aktif')
    ], required=True)
    @api.model
    def create (self, vals):
        if vals.get('bangsal_id', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record  = self.search([('bangsal_id', 'like', f'BSL/{current_year}/%')], order = 'id desc', limit=1)

            if last_record:
                last_id = last_record.bangsal_id
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            vals['bangsal_id'] = f'BSL/{current_year}/{new_number:03d}'
        return super(Bangsal, self).create(vals)
            