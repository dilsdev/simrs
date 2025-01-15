from odoo import models, fields

class Diagnosa_pasien(models.Model):
    _name = 'cdn.diagnosa_pasien'
    _description = 'Diagnosa Pasien'
    _rec_name = 'no_rawat'
    _sql_constraints = [
        ('diagnosa_pasien_unique', 'unique(no_rawat, status)', 'The combination of No Rawat, Kd Penyakit, and Status must be unique.')
    ]

    no_rawat = fields.Char('No Rawat', required=True)
    status = fields.Selection([
        ('Ralan', 'Rawat Jalan'),
        ('Ranap', 'Rawat Inap')
    ], string='Status', required=True)
    prioritas = fields.Integer('Prioritas', required=True)
    status_penyakit = fields.Selection([
        ('Lama', 'Lama'),
        ('Baru', 'Baru')
    ], string='Status Penyakit')

    # Relasi dengan model reg_periksa
    reg_periksa_id = fields.Many2one('reg.periksa', string='No Rawat', ondelete='cascade', required=True)
    
    # Relasi dengan model penyakit
    penyakit_id = fields.Many2one('cdn.penyakit', string='Kode Penyakit', ondelete='cascade', required=True)

    _sql_constraints = [
        ('diagnosa_pasien_unique', 'unique(no_rawat, status)', 'The combination of No Rawat, Kd Penyakit, and Status must be unique.')
    ]
