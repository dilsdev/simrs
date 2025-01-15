from odoo import api, fields, models

class Jns_perawatan(models.Model):
    _name = 'cdn.jns_perawatan'
    _description = 'Jenis Perawatan'
    _rec_name = 'kd_jenis_prw'
    
    kd_jenis_prw = fields.Char('Kode Jenis Perawatan', required=True, size=15, index=True)
    nm_perawatan = fields.Char('Nama Perawatan', size=80)
    kd_kategori = fields.Char('Kode Kategori', size=5, index=True)
    material = fields.Float('Material', digits=(16, 2), default=0.0)
    bhp = fields.Float('BHP', required=True, digits=(16, 2))
    tarif_tindakandr = fields.Float('Tarif Tindakan DR', digits=(16, 2), default=0.0)
    tarif_tindakanpr = fields.Float('Tarif Tindakan PR', digits=(16, 2), default=0.0)
    kso = fields.Float('KSO', digits=(16, 2), default=0.0)
    menejemen = fields.Float('Menejemen', digits=(16, 2), default=0.0)
    total_byrdr = fields.Float('Total Bayar DR', digits=(16, 2), default=0.0)
    total_byrpr = fields.Float('Total Bayar PR', digits=(16, 2), default=0.0)
    total_byrdrpr = fields.Float('Total Bayar DR/PR', required=True, digits=(16, 2))
    kd_pj = fields.Char('Kode PJ', size=3, required=True, index=True)
    kd_poli = fields.Char('Kode Poli', size=5, required=True, index=True)
    status = fields.Selection([('0', 'Non-Aktif'), ('1', 'Aktif')], 'Status', required=True, default='1')

    # Foreign Keys (Relationships)
    kategori_id = fields.Many2one('kategori.perawatan', string='Kategori Perawatan', ondelete='cascade', index=True)
    kd_pj = fields.Many2one('cdn.penanggung_jawab', string='Penjab', ondelete='cascade', index=True)
    kd_poli = fields.Many2one('cdn.poliklinik', string='Poliklinik', ondelete='cascade', index=True)

    _sql_constraints = [
        ('kd_jenis_prw_unique', 'UNIQUE(kd_jenis_prw)', 'Kode Jenis Perawatan harus unik!'),
    ]
