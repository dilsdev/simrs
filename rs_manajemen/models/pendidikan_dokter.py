from odoo import api, fields, models

class PendidikanDokter(models.Model):
    _name = 'cdn.pendidikan_dokter'
    _description = 'Riwayat Pendidikan Dokter'

    name = fields.Char(string='Nama Institusi')
    jenjang = fields.Selection([
        ('sd', 'SD/MI'),
        ('smp', 'SMP/MTS'),
        ('sma', 'SMA/MA'),
        ('diploma', 'D1/D2/D3'),
        ('sarjana', 'D4/S1'),
        ('pasca', 'S2/S3'),
        ('lainnya', 'Lainnya/Non Formal')
    ], string='Jenjang Pendidikan')
    fakultas = fields.Char(string='Fakultas/Jurusan')
    gelar = fields.Char(string='Gelar')
    karya_ilmiah = fields.Char(string='Karya Ilmiah (Skripsi/Tesis/Disertasi)')
    lulus = fields.Date(string='Tanggal Lulus')

    doctor_id = fields.Many2one('cdn.doctor', string="Dokter")
