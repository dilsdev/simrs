from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class Rawat_jalan(models.Model):
    _name = 'cdn.rawat_jalan'
    _description = 'Rawat Jalan'
    _rec_name = 'no_rawat'

    # Existing fields remain the same until create method
    no_rawat = fields.Many2one('cdn.reg_periksa', string='No Rawat', ondelete='cascade')
    kd_dokter = fields.Many2one(related='no_rawat.kd_dokter', string='Dokter', readonly=True, store=True)
    no_rkm_medis = fields.Many2one(related='no_rawat.no_rkm_medis', string='Rekam Medis', readonly=True, store=True)
    pasien = fields.Char(related='no_rkm_medis.name', string='Pasien', readonly=True, store=True)

    @api.onchange('no_rawat')
    def _onchange_no_rawat(self):
        if self.no_rawat:
            self.kd_dokter = self.no_rawat.kd_dokter
            self.no_rkm_medis = self.no_rawat.no_rkm_medis
            self.pasien = self.no_rkm_medis.name


    rawat_jl_dr_no_rawat = fields.Char(string='No Rawat', index=True)
    rawat_jl_dr_kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan', index=True)
    rawat_jl_dr_kd_dokter = fields.Many2one('cdn.doctor', string='Kode Dokter', ondelete='cascade', index=True)
    rawat_jl_dr_tgl_perawatan = fields.Date(string='Tanggal Perawatan',)
    rawat_jl_dr_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    rawat_jl_dr_material = fields.Float(string='Material',)
    rawat_jl_dr_bhp = fields.Float(string='BHP',)
    rawat_jl_dr_tarif_tindakandr = fields.Float(string='Tarif Tindakan Dokter',)
    rawat_jl_dr_kso = fields.Float(string='KSO')
    rawat_jl_dr_menejemen = fields.Float(string='Manajemen')
    rawat_jl_dr_biaya_rawat = fields.Float(string='Biaya Rawat')
    rawat_jl_dr_stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar')

    _sql_constraints = [
        ('rawat_jl_dr_uniq', 'unique(rawat_jl_dr_no_rawat, rawat_jl_dr_kd_jenis_prw, rawat_jl_dr_kd_dokter, rawat_jl_dr_tgl_perawatan, rawat_jl_dr_jam_rawat)',
         'Kombinasi No Rawat, Kode Jenis Perawatan, Kode Dokter, Tanggal Perawatan, dan Jam Rawat harus unik!')
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

#   Rawat jalan Pr

    rawat_jl_pr_no_rawat = fields.Char(string='No Rawat', index=True)
    rawat_jl_pr_kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan', index=True)
    rawat_jl_pr_nip = fields.Char(string='NIP', index=True)
    rawat_jl_pr_tgl_perawatan = fields.Date(string='Tanggal Perawatan',)
    rawat_jl_pr_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    rawat_jl_pr_material = fields.Float(string='Material',)
    rawat_jl_pr_bhp = fields.Float(string='BHP',)
    rawat_jl_pr_tarif_tindakanpr = fields.Float(string='Tarif Tindakan Petugas',)
    rawat_jl_pr_kso = fields.Float(string='KSO')
    rawat_jl_pr_menejemen = fields.Float(string='Manajemen')
    rawat_jl_pr_biaya_rawat = fields.Float(string='Biaya Rawat')
    rawat_jl_pr_stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar')

    _sql_constraints = [
        ('rawat_jl_pr_uniq', 'unique(rawat_jl_pr_no_rawat, rawat_jl_pr_kd_jenis_prw, rawat_jl_pr_nip, rawat_jl_pr_tgl_perawatan, rawat_jl_pr_jam_rawat)', 'Kombinasi No Rawat, Kode Jenis Perawatan, NIP, Tanggal Perawatan, dan Jam Rawat harus unik!')
    ]

    @api.constrains('rawat_jl_pr_material', 'rawat_jl_pr_bhp', 'rawat_jl_pr_tarif_tindakanpr', 'rawat_jl_pr_kso', 'rawat_jl_pr_menejemen', 'rawat_jl_pr_biaya_rawat')
    def _check_numeric_fields(self):
        for record in self:
            if record.rawat_jl_pr_material < 0:
                raise ValidationError("Material tidak boleh bernilai negatif.")
            if record.rawat_jl_pr_bhp < 0:
                raise ValidationError("BHP tidak boleh bernilai negatif.")
            if record.rawat_jl_pr_tarif_tindakanpr < 0:
                raise ValidationError("Tarif Tindakan Petugas tidak boleh bernilai negatif.")
            if record.rawat_jl_pr_kso is not None and record.rawat_jl_pr_kso < 0:
                raise ValidationError("KSO tidak boleh bernilai negatif.")
            if record.rawat_jl_pr_menejemen is not None and record.rawat_jl_pr_menejemen < 0:
                raise ValidationError("Manajemen tidak boleh bernilai negatif.")
            if record.rawat_jl_pr_biaya_rawat is not None and record.rawat_jl_pr_biaya_rawat < 0:
                raise ValidationError("Biaya Rawat tidak boleh bernilai negatif.")
        

#   pemeriksaan_ralan
    pemeriksaan_ralan_no_rawat = fields.Char(string='No Rawat', index=True)
    pemeriksaan_ralan_tgl_perawatan = fields.Date(string='Tanggal Perawatan',)
    pemeriksaan_ralan_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    pemeriksaan_ralan_suhu_tubuh = fields.Char(string='Suhu Tubuh', size=5)
    pemeriksaan_ralan_tensi = fields.Char(string='Tensi', size=8,)
    pemeriksaan_ralan_nadi = fields.Char(string='Nadi', size=3)
    pemeriksaan_ralan_respirasi = fields.Char(string='Respirasi', size=3)
    pemeriksaan_ralan_tinggi = fields.Char(string='Tinggi', size=5)
    pemeriksaan_ralan_berat = fields.Char(string='Berat', size=5)
    pemeriksaan_ralan_spo2 = fields.Char(string='SPO2', size=3,)
    pemeriksaan_ralan_gcs = fields.Char(string='GCS', size=10)
    pemeriksaan_ralan_kesadaran = fields.Selection([
        ('Compos Mentis', 'Compos Mentis / Sadar dan berfungsi normal'),
        ('Somnolence', 'Somnolence / Mengantuk, tetapi dapat dibangunkan'),
        ('Sopor', 'Sopor / Tidur yang dalam, sulit dibangunkan'),
        ('Coma', 'Coma / Tidak sadar, tidak responsif'),
        ('Alert', 'Alert / Sadar dan responsif'),
        ('Confusion', 'Confusion / Bingung, tidak dapat berfungsi dengan baik'),
        ('Voice', 'Voice / Responsif terhadap suara'),
        ('Pain', 'Pain / Responsif terhadap rasa sakit'),
        ('Unresponsive', 'Unresponsive / Tidak responsif sama sekali'),
        ('Apatis', 'Apatis / Tidak peduli, tidak ada respons emosional'),
        ('Delirium', 'Delirium / Kebingungan akut, perubahan kesadaran'),
    ], string='Kesadaran',)
    pemeriksaan_ralan_keluhan = fields.Text(string='Keluhan', size=2000)
    pemeriksaan_ralan_pemeriksaan = fields.Text(string='Pemeriksaan', size=2000)
    pemeriksaan_ralan_alergi = fields.Char(string='Alergi', size=80)
    pemeriksaan_ralan_lingkar_perut = fields.Char(string='Lingkar Perut', size=5)
    pemeriksaan_ralan_rtl = fields.Text(string='RTL', size=2000)
    pemeriksaan_ralan_penilaian = fields.Text(string='Penilaian', size=2000)
    pemeriksaan_ralan_instruksi = fields.Text(string='Instruksi', size=2000)
    pemeriksaan_ralan_evaluasi = fields.Text(string='Evaluasi', size=2000)
    pemeriksaan_ralan_nip = fields.Char(string='NIP', index=True)

    _sql_constraints = [
        ('pemeriksaan_ralan_uniq', 'unique(pemeriksaan_ralan_no_rawat, pemeriksaan_ralan_tgl_perawatan, pemeriksaan_ralan_jam_rawat)', 'Kombinasi No Rawat, Tanggal Perawatan, dan Jam Rawat harus unik!')
    ]

    @api.constrains('pemeriksaan_ralan_suhu_tubuh', 'pemeriksaan_ralan_tensi', 'pemeriksaan_ralan_nadi', 'pemeriksaan_ralan_respirasi', 'pemeriksaan_ralan_tinggi', 'pemeriksaan_ralan_berat', 'pemeriksaan_ralan_spo2', 'pemeriksaan_ralan_gcs', 'pemeriksaan_ralan_lingkar_perut')
    def _check_field_constraints(self):
        for record in self:
            if record.pemeriksaan_ralan_suhu_tubuh and not record.pemeriksaan_ralan_suhu_tubuh.replace('.', '').isdigit():
                raise ValidationError("Suhu Tubuh harus berupa angka valid.")
            if record.pemeriksaan_ralan_tensi and not record.pemeriksaan_ralan_tensi.replace('/', '').isdigit():
                raise ValidationError("Tensi harus berupa angka valid dengan format '120/80'.")
            if record.pemeriksaan_ralan_nadi and not record.pemeriksaan_ralan_nadi.isdigit():
                raise ValidationError("Nadi harus berupa angka.")
            if record.pemeriksaan_ralan_respirasi and not record.pemeriksaan_ralan_respirasi.isdigit():
                raise ValidationError(" Respirasi harus berupa angka.")
            if record.pemeriksaan_ralan_tinggi and not record.pemeriksaan_ralan_tinggi.isdigit():
                raise ValidationError("Tinggi harus berupa angka.")
            if record.pemeriksaan_ralan_berat and not record.pemeriksaan_ralan_berat.isdigit():
                raise ValidationError("Berat harus berupa angka.")
            if record.pemeriksaan_ralan_spo2 and not record.pemeriksaan_ralan_spo2.isdigit():
                raise ValidationError("SPO2 harus berupa angka.")
            if record.pemeriksaan_ralan_lingkar_perut and not record.pemeriksaan_ralan_lingkar_perut.isdigit():
                raise ValidationError("Lingkar Perut harus berupa angka.")


    # diagnosa
    _sql_constraints = [
    ('diagnosa_pasien_unique', 'unique(diagnosa_pasien_no_rawat, diagnosa_pasien_status)', 'The combination of No Rawat and Status must be unique.')
    ]

    diagnosa_pasien_no_rawat = fields.Char('No Rawat',)
    diagnosa_pasien_status = fields.Selection([
        ('Ralan', 'Rawat Jalan'),
        ('Ranap', 'Rawat Inap')
    ], string='Status',)
    diagnosa_pasien_prioritas = fields.Integer('Prioritas',)
    diagnosa_pasien_status_penyakit = fields.Selection([
        ('Lama', 'Lama'),
        ('Baru', 'Baru')
    ], string='Status Penyakit')

    diagnosa_pasien_reg_periksa_id = fields.Many2one('reg.periksa', string='No Rawat', ondelete='cascade',)
    diagnosa_pasien_penyakit_id = fields.Many2one('cdn.penyakit', string='Kode Penyakit', ondelete='cascade',)



    @api.model
    def create(self, vals):
    

        # Mengambil data Many2one terkait
        kd_jenis_prw = self.env['cdn.jns_perawatan'].browse(vals.get('rawat_jl_dr_kd_jenis_prw'))
        kd_dokter = self.env['cdn.doctor'].browse(vals.get('rawat_jl_dr_kd_dokter'))

        # Membuat record di tabel utama
        reg_periksa = super(Rawat_jalan, self).create(vals)

        # Create rawat_jl_dr record
        self.env['cdn.rawat_jl_dr'].create({
            'no_rawat': vals.get('rawat_jl_dr_no_rawat'),
            'kd_jenis_prw': kd_jenis_prw.id,
            'kd_dokter': kd_dokter.id,
            'tgl_perawatan': vals.get('rawat_jl_dr_tgl_perawatan'),
            'jam_rawat': vals.get('rawat_jl_dr_jam_rawat'),
            'material': vals.get('rawat_jl_dr_material', 0.0),
            'bhp': vals.get('rawat_jl_dr_bhp', 0.0),
            'tarif_tindakandr': vals.get('rawat_jl_dr_tarif_tindakandr', 0.0),
            'kso': vals.get('rawat_jl_dr_kso', 0.0),
            'menejemen': vals.get('rawat_jl_dr_menejemen', 0.0),
            'biaya_rawat': vals.get('rawat_jl_dr_biaya_rawat', 0.0),
            'stts_bayar': vals.get('rawat_jl_dr_stts_bayar', 'Belum'),
        })

        # Create rawat_jl_pr record
        if vals.get('rawat_jl_pr_no_rawat'):
            self.env['cdn.rawat_jl_pr'].create({
                'no_rawat': vals.get('rawat_jl_pr_no_rawat'),
                'kd_jenis_prw': kd_jenis_prw.id,
                'nip': vals.get('rawat_jl_pr_nip'),
                'tgl_perawatan': vals.get('rawat_jl_pr_tgl_perawatan'),
                'jam_rawat': vals.get('rawat_jl_pr_jam_rawat'),
                'material': vals.get('rawat_jl_pr_material', 0.0),
                'bhp': vals.get('rawat_jl_pr_bhp', 0.0),
                'tarif_tindakanpr': vals.get('rawat_jl_pr_tarif_tindakanpr', 0.0),
                'kso': vals.get('rawat_jl_pr_kso', 0.0),
                'menejemen': vals.get('rawat_jl_pr_menejemen', 0.0),
                'biaya_rawat': vals.get('rawat_jl_pr_biaya_rawat', 0.0),
                'stts_bayar': vals.get('rawat_jl_pr_stts_bayar', 'Belum'),
            })

        # Create diagnosa_pasien record
        if vals.get('diagnosa_pasien_penyakit_id'):
            self.env['cdn.diagnosa_pasien'].create({
                'no_rawat': vals.get('diagnosa_pasien_no_rawat'),
                'status': vals.get('diagnosa_pasien_status', 'Ralan'),
                'prioritas': vals.get('diagnosa_pasien_prioritas', 1),
                'status_penyakit': vals.get('diagnosa_pasien_status_penyakit', 'Baru'),
                'reg_periksa_id': vals.get('diagnosa_pasien_reg_periksa_id'),
                'penyakit_id': vals.get('diagnosa_pasien_penyakit_id'),
            })

        return reg_periksa

    # Menambahkan method untuk menghitung total biaya
    @api.depends('rawat_jl_dr_material', 'rawat_jl_dr_bhp', 'rawat_jl_dr_tarif_tindakandr', 
                'rawat_jl_dr_kso', 'rawat_jl_dr_menejemen')
    def _compute_total_biaya_dr(self):
        for record in self:
            record.rawat_jl_dr_biaya_rawat = (
                record.rawat_jl_dr_material +
                record.rawat_jl_dr_bhp +
                record.rawat_jl_dr_tarif_tindakandr +
                record.rawat_jl_dr_kso +
                record.rawat_jl_dr_menejemen
            )

    @api.depends('rawat_jl_pr_material', 'rawat_jl_pr_bhp', 'rawat_jl_pr_tarif_tindakanpr', 
                'rawat_jl_pr_kso', 'rawat_jl_pr_menejemen')
    def _compute_total_biaya_pr(self):
        for record in self:
            record.rawat_jl_pr_biaya_rawat = (
                record.rawat_jl_pr_material +
                record.rawat_jl_pr_bhp +
                record.rawat_jl_pr_tarif_tindakanpr +
                record.rawat_jl_pr_kso +
                record.rawat_jl_pr_menejemen
            )

    # Add method untuk validasi jam
    @api.constrains('rawat_jl_dr_jam_rawat', 'rawat_jl_pr_jam_rawat', 'pemeriksaan_ralan_jam_rawat')
    def _check_jam_rawat(self):
        for record in self:
            fields_to_check = [
                ('rawat_jl_dr_jam_rawat', 'Jam Rawat Dokter'),
                ('rawat_jl_pr_jam_rawat', 'Jam Rawat Perawat'),
                ('pemeriksaan_ralan_jam_rawat', 'Jam Rawat Pemeriksaan')
            ]
            
            for field, name in fields_to_check:
                value = getattr(record, field, False)
                if value and (value < 0 or value >= 24):
                    raise ValidationError(f"{name} harus antara 0 dan 24")

    # Method untuk memvalidasi tanggal
    @api.constrains('rawat_jl_dr_tgl_perawatan', 'rawat_jl_pr_tgl_perawatan', 'pemeriksaan_ralan_tgl_perawatan')
    def _check_tanggal_perawatan(self):
        today = fields.Date.today()
        for record in self:
            fields_to_check = [
                ('rawat_jl_dr_tgl_perawatan', 'Tanggal Perawatan Dokter'),
                ('rawat_jl_pr_tgl_perawatan', 'Tanggal Perawatan Perawat'),
                ('pemeriksaan_ralan_tgl_perawatan', 'Tanggal Pemeriksaan')
            ]
            
            for field, name in fields_to_check:
                value = getattr(record, field, False)
                if value and value > today:
                    raise ValidationError(f"{name} tidak boleh lebih dari tanggal hari ini")

    def action_confirm(self):
        for record in self:
            if record.rawat_jl_dr_stts_bayar == 'Belum':
                record.rawat_jl_dr_stts_bayar = 'Sudah'
            if record.rawat_jl_pr_stts_bayar == 'Belum':
                record.rawat_jl_pr_stts_bayar = 'Sudah'
        return True

    def action_cancel(self):
        for record in self:
            if record.rawat_jl_dr_stts_bayar == 'Sudah':
                record.rawat_jl_dr_stts_bayar = 'Belum'
            if record.rawat_jl_pr_stts_bayar == 'Sudah':
                record.rawat_jl_pr_stts_bayar = 'Belum'
        return True