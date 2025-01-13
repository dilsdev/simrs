from odoo import models, fields, api

class Reg_periksa(models.Model):
    _name = 'cdn.reg_periksa'
    _description = 'Registrasi Pemeriksaan'
    _rec_name = 'no_rawat'

    no_reg = fields.Char(string='No Registrasi', size=8)
    no_rawat = fields.Char(string='No Rawat', size=17, required=True, index=True)
    tgl_registrasi = fields.Date(string='Tanggal Registrasi')
    jam_reg = fields.Float(string='Jam Registrasi', help="Gunakan format desimal untuk jam, misalnya 13.30 untuk 13:30.")
    kd_dokter = fields.Many2one('cdn.doctor', string='Kode Dokter', ondelete='cascade', index=True)
    no_rkm_medis = fields.Many2one('cdn.pasien', string='No Rekam Medis', ondelete='cascade', index=True)
    kd_poli = fields.Many2one('cdn.poliklinik', string='Kode Poliklinik', ondelete='cascade', index=True)
    p_jawab = fields.Char(string='Penanggung Jawab', readonly=True)
    almt_pj = fields.Char(string='Alamat Penanggung Jawab', readonly=True)
    hubunganpj = fields.Char(string='Hubungan dengan Penanggung Jawab', readonly=True)
    biaya_reg = fields.Float(string='Biaya Registrasi')
    stts = fields.Selection([
        ('Belum', 'Belum'),
        ('Sudah', 'Sudah'),
        ('Batal', 'Batal'),
        ('Berkas Diterima', 'Berkas Diterima'),
        ('Dirujuk', 'Dirujuk'),
        ('Meninggal', 'Meninggal'),
        ('Dirawat', 'Dirawat'),
        ('Pulang Paksa', 'Pulang Paksa')
    ], string='Status')
    stts_daftar = fields.Selection([
        ('-', '-'),
        ('Lama', 'Lama'),
        ('Baru', 'Baru')
    ], string='Status Daftar', required=True)
    status_lanjut = fields.Selection([
        ('Ralan', 'Rawat Jalan'),
        ('Ranap', 'Rawat Inap')
    ], string='Status Lanjut', required=True, index=True)
    kd_pj = fields.Many2one('cdn.penanggung_jawab', string='Kode Penjamin', ondelete='cascade', index=True)
    umurdaftar = fields.Integer(string='Umur Daftar')
    sttsumur = fields.Selection([
        ('Th', 'Tahun'),
        ('Bl', 'Bulan'),
        ('Hr', 'Hari')
    ], string='Status Umur')
    status_bayar = fields.Selection([
        ('Sudah Bayar', 'Sudah Bayar'),
        ('Belum Bayar', 'Belum Bayar')
    ], string='Status Bayar', required=True, index=True)
    status_poli = fields.Selection([
        ('Lama', 'Lama'),
        ('Baru', 'Baru')
    ], string='Status Poliklinik', required=True)

    _sql_constraints = [
        ('no_rawat_uniq', 'unique(no_rawat)', 'Nomor Rawat harus unik!'),
    ]

    @api.onchange('no_rkm_medis')
    def _onchange_no_rkm_medis(self):
        if self.no_rkm_medis:
            self.p_jawab = self.no_rkm_medis.p_jawab
            self.hubunganpj = self.no_rkm_medis.keluarga
            self.almt_pj = self.no_rkm_medis.alamatpj

    @api.onchange('stts_daftar', 'kd_poli')
    def _onchange_stts_daftar(self):
        if self.stts_daftar and self.kd_poli:
            if self.kd_poli.exists():  # Pastikan kd_poli valid
                if self.stts_daftar == 'Lama':
                    self.biaya_reg = self.kd_poli.registrasi_lama
                elif self.stts_daftar == 'Baru':
                    self.biaya_reg = self.kd_poli.registrasi
            else:
                self.biaya_reg = 0.0
        else:
            self.biaya_reg = 0.0
    
    def action_confirm(self):
        for record in self:
            record.stts = 'Sudah'

    def action_cancel(self):
        for record in self:
            record.stts = 'Batal'
