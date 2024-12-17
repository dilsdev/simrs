# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Cacat_fisik(models.Model):
    _name = 'cdn.cacat_fisik'
    _description = 'Cacat Fisik'

    cacat_id = fields.Char(string='ID Cacat', required=True, copy=False, readonly=True, default='CCT/20XX/XXX')
    name= fields.Char(string='Nama', required=True)

    @api.model
    def create(self, vals):
        if vals.get('cacat_id', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record = self.search([('cacat_id', 'like', f'CCT/{current_year}/%')], order='id desc', limit=1)

            if last_record:
                last_id = last_record.cacat_id
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1

            vals['cacat_id'] = f'CCT/{current_year}/{new_number:03d}'
        return super(Cacat_fisik, self).create(vals)
