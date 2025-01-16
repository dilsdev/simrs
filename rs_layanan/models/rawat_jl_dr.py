from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Rawat_jl_dr(models.Model):
    _name = 'cdn.rawat_jl_dr'
    _description = 'Rawat Jalan Dokter'
    _rec_name = 'no_rawat'

    no_rawat = fields.Char(string='No Rawat', index=True)
    kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan', index=True)
    kd_dokter = fields.Many2one('cdn.doctor', string='Kode Dokter', ondelete='cascade', index=True)
    tgl_perawatan = fields.Date(string='Tanggal Perawatan')
    jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    material = fields.Float(string='Material')
    bhp = fields.Float(string='BHP')
    tarif_tindakandr = fields.Float(string='Tarif Tindakan Dokter')
    kso = fields.Float(string='KSO')
    menejemen = fields.Float(string='Manajemen')
    biaya_rawat = fields.Float(string='Biaya Rawat')
    stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar')

    _sql_constraints = [
        ('rawat_jl_dr_uniq', 'unique(no_rawat, kd_jenis_prw, kd_dokter, tgl_perawatan, jam_rawat)', 'Kombinasi No Rawat, Kode Jenis Perawatan, Kode Dokter, Tanggal Perawatan, dan Jam Rawat harus unik!')
    ]

    @api.constrains('material', 'bhp', 'tarif_tindakandr', 'kso', 'menejemen', 'biaya_rawat')
    def _check_numeric_fields(self):
        for record in self:
            if record.material < 0:
                raise ValidationError("Material tidak boleh bernilai negatif.")
            if record.bhp < 0:
                raise ValidationError("BHP tidak boleh bernilai negatif.")
            if record.tarif_tindakandr < 0:
                raise ValidationError("Tarif Tindakan Dokter tidak boleh bernilai negatif.")
            if record.kso is not None and record.kso < 0:
                raise ValidationError("KSO tidak boleh bernilai negatif.")
            if record.menejemen is not None and record.menejemen < 0:
                raise ValidationError("Manajemen tidak boleh bernilai negatif.")
            if record.biaya_rawat is not None and record.biaya_rawat < 0:
                raise ValidationError("Biaya Rawat tidak boleh bernilai negatif.")

    @api.model
    def create(self, vals):
        # Logika tambahan jika diperlukan saat membuat record baru
        return super(Rawat_jl_dr, self).create(vals)

    def write(self, vals):
        # Logika tambahan jika diperlukan saat mengupdate record
        return super(Rawat_jl_dr, self).write(vals)
