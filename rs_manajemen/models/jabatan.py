from odoo import api, fields, models
from odoo.exceptions import UserError

class Jabatan(models.Model):
    _name = 'cdn.jabatan'
    _description = 'Jabatan'

    name = fields.Char('Nama Jabatan', required=True)
    kode_jabatan = fields.Char('Kode Jabatan', required=True)
    deskripsi = fields.Text('Deskripsi Jabatan')

