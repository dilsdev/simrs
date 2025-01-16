from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
class RegPeriksa(models.Model):
    _name = 'cdn.reg_periksa'
    _description = 'Registrasi Pemeriksaan'
    _rec_name = 'no_rawat'

    no_reg = fields.Char(string='No Registrasi', required=False) 
    cacat_id = fields.Char(string='ID Cacat', required=True, copy=False, readonly=True, default='CCT/20XX/XXX')
    no_rawat = fields.Char(string='No Rawat', required=True, index=True)
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
    ], string='Status', default='Belum')
    
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
            self.p_jawab = self.no_rkm_medis.p_jawab or ''
            self.hubunganpj = self.no_rkm_medis.keluarga or ''
            self.almt_pj = self.no_rkm_medis.alamatpj or ''
        else:
            self.p_jawab = ''
            self.hubunganpj = ''
            self.almt_pj = ''

    @api.onchange('stts_daftar', 'kd_poli')
    def _onchange_stts_daftar(self):
        if self.stts_daftar and self.kd_poli:
            if self.kd_poli.id:  # Pastikan kd_poli memiliki ID yang valid
                if self.stts_daftar == 'Lama':
                    self.biaya_reg = self.kd_poli.registrasi_lama or 0.0
                elif self.stts_daftar == 'Baru':
                    self.biaya_reg = self.kd_poli.registrasi or 0.0
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

    @api.model
    def create(self, vals):
        # Pastikan no_rawat diisi
        if not vals.get('no_rawat'):
            raise ValidationError("No Rawat wajib diisi. a")

        # Membuat record di 'cdn.reg_periksa' terlebih dahulu
        reg_periksa = super(RegPeriksa, self).create(vals)

        # Membuat record baru di 'cdn.rawat_jalan' setelah 'cdn.reg_periksa' berhasil dibuat
        self.env['cdn.rawat_jalan'].create({
            'no_rawat': vals.get('no_rawat'),  # Menggunakan ID dari 'cdn.reg_periksa'
            'kd_dokter': reg_periksa.kd_dokter.id,
            'no_rkm_medis': reg_periksa.no_rkm_medis.id,
            'pasien': reg_periksa.no_rkm_medis.name,  # Nama pasien diambil dari 'cdn.pasien'
        })

        return reg_periksa
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