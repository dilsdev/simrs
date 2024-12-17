# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Suku(models.Model):
    _name = 'cdn.suku'
    _description = 'Suku'

    suku_id = fields.Char(string='ID Suku', required=True, copy=False, readonly=True, default='SKU/20XX/XXX')
    name= fields.Char(string='Nama', required=True)

    @api.model
    def create(self, vals):
        if vals.get('suku_id', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record = self.search([('suku_id', 'like', f'SKU/{current_year}/%')], order='id desc', limit=1)

            if last_record:
                last_id = last_record.suku_id
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1

            vals['suku_id'] = f'SKU/{current_year}/{new_number:03d}'
        return super(Suku, self).create(vals)
