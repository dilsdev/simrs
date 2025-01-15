from odoo import models, fields, api

class Rawat_jalan(models.Model):
    _name = 'cdn.rawat_jalan'
    _description = 'Rawat Jalan'

    no_rawat = fields.Many2one('cdn.reg_periksa', string='No Rawat', readonly=True,)
    kd_dokter = fields.Many2one(related='no_rawat.kd_dokter', string='Dokter', readonly=True, store=True)
    no_rkm_medis = fields.Many2one(related='no_rawat.no_rkm_medis', string='Rekam Medis', readonly=True, store=True)
    pasien = fields.Char(related='no_rkm_medis.name', string='Pasien', readonly=True, store=True)

    @api.onchange('no_rawat')
    def _onchange_no_rawat(self):
        if self.no_rawat:
            self.kd_dokter = self.no_rawat.kd_dokter
            self.no_rkm_medis = self.no_rawat.no_rkm_medis
            self.pasien = self.no_rkm_medis.name


    # Rawat Jalan Dokter  
    rawat_jl_dr_no_rawat = fields.Char(string='No Rawat', required=True, index=True)
    rawat_jl_dr_kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan',required=True, index=True)
    rawat_jl_dr_kd_dokter = fields.Many2one('cdn.doctor', string='Kode Dokter', ondelete='cascade', index=True)
    rawat_jl_dr_tgl_perawatan = fields.Date(string='Tanggal Perawatan', required=True)
    rawat_jl_dr_jam_rawat = fields.Float(string='Jam Rawat', required=True, help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    rawat_jl_dr_material = fields.Float(string='Material', required=True)
    rawat_jl_dr_bhp = fields.Float(string='BHP', required=True)
    rawat_jl_dr_tarif_tindakandr = fields.Float(string='Tarif Tindakan Dokter', required=True)
    rawat_jl_dr_kso = fields.Float(string='KSO')
    rawat_jl_dr_menejemen = fields.Float(string='Manajemen')
    rawat_jl_dr_biaya_rawat = fields.Float(string='Biaya Rawat')
    rawat_jl_dr_stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar')

    _sql_constraints = [
        ('rawat_jl_dr_uniq', 'unique(rawat_jl_dr_no_rawat, rawat_jl_dr_kd_jenis_prw, rawat_jl_dr_kd_dokter, rawat_jl_dr_tgl_perawatan, rawat_jl_dr_jam_rawat)', 'Kombinasi No Rawat, Kode Jenis Perawatan, Kode Dokter, Tanggal Perawatan, dan Jam Rawat harus unik!')
    ]

    @api.constrains('rawat_jl_dr_material', 'rawat_jl_dr_bhp', 'rawat_jl_dr_tarif_tindakandr', 'rawat_jl_dr_kso', 'rawat_jl_dr_menejemen', 'rawat_jl_dr_biaya_rawat')
    def _check_numeric_fields(self):
        for record in self:
            if record.rawat_jl_dr_material < 0:
                raise ValidationError("Material tidak boleh bernilai negatif.")
            if record.rawat_jl_dr_bhp < 0:
                raise ValidationError("BHP tidak boleh bernilai negatif.")
            if record.rawat_jl_dr_tarif_tindakandr < 0:
                raise ValidationError("Tarif Tindakan Dokter tidak boleh bernilai negatif.")
            if record.rawat_jl_dr_kso is not None and record.rawat_jl_dr_kso < 0:
                raise ValidationError("KSO tidak boleh bernilai negatif.")
            if record.rawat_jl_dr_menejemen is not None and record.rawat_jl_dr_menejemen < 0:
                raise ValidationError("Manajemen tidak boleh bernilai negatif.")
            if record.rawat_jl_dr_biaya_rawat is not None and record.rawat_jl_dr_biaya_rawat < 0:
                raise ValidationError("Biaya Rawat tidak boleh bernilai negatif.")










@api.model
def create(self, vals):
    # Membuat record di 'cdn.rawat_jalan' terlebih dahulu
    reg_periksa = super(Rawat_jalan, self).create(vals)

    # Membuat record baru di 'cdn.rawat_jl_dr' setelah 'cdn.rawat_jalan' berhasil dibuat
    self.env['cdn.rawat_jl_dr'].create({
        'no_rawat': vals.get('rawat_jl_dr_no_rawat'),
        'kd_jenis_prw': vals.get('rawat_jl_dr_kd_jenis_prw'),
        'kd_dokter': vals.get('rawat_jl_dr_kd_dokter'),
        'tgl_perawatan': vals.get('rawat_jl_dr_tgl_perawatan'),
        'jam_rawat': vals.get('rawat_jl_dr_jam_rawat'),
        'material': vals.get('rawat_jl_dr_material'),
        'bhp': vals.get('rawat_jl_dr_bhp'),
        'tarif_tindakandr': vals.get('rawat_jl_dr_tarif_tindakandr'),
        'kso': vals.get('rawat_jl_dr_kso'),
        'menejemen': vals.get('rawat_jl_dr_menejemen'),
        'biaya_rawat': vals.get('rawat_jl_dr_biaya_rawat'),
        'stts_bayar': vals.get('rawat_jl_dr_stts_bayar'),
    })

    return reg_periksa
