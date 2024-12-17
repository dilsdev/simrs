from odoo import models, fields

class Poliklinik(models.Model):
    _name = 'cdn.poliklinik'
    _description = 'Data Poliklinik'

    kode_poliklinik = fields.Char(string="Kode Poliklinik", required=True)
    name = fields.Char(string="Nama Poliklinik", required=True)
    registrasi = fields.Integer(string="Jumlah Registrasi")
    registrasi_lama = fields.Integer(string="Jumlah Registrasi Lama")
    status_aktif = fields.Boolean(string="Status Aktif", default=True)
