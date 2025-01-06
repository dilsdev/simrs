from odoo import models, fields, api
from datetime import datetime

class Pasien(models.Model):
    _name = 'cdn.pasien'
    _description = 'Data Pasien'
    _inherits = {'res.partner': 'partner_id'}

    no_rkm_medis = fields.Char(string='No Rekam Medis', required=True, copy=False, readonly=True, default='NRM/20XX/XXX')
    # name = fields.Char(string="Nama Pasien", required=True)  # Nama pasien harus required
    partner_id = fields.Many2one('res.partner', string="Contact", required=False, ondelete="cascade")
    no_ktp = fields.Char(string="Nomor KTP", required=True)  # KTP penting untuk identifikasi
    jk = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], string="Jenis Kelamin", required=True)  # Jenis kelamin penting untuk medis
    tmp_lahir = fields.Char(string="Tempat Lahir", required=True)  # Tempat lahir penting untuk identifikasi
    tgl_lahir = fields.Date(string="Tanggal Lahir", required=True)  # Tanggal lahir penting untuk medis
    nm_ibu = fields.Char(string="Nama Ibu", required=True)  # Tetap required untuk verifikasi
    alamat = fields.Text(string="Alamat", required=True)  # Alamat penting untuk kunjungan/kontak
    gol_darah = fields.Selection([('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB'), ('-', '-')], string="Golongan Darah")
    pekerjaan = fields.Char(string="Pekerjaan")
    stts_nikah = fields.Selection([
        ('BELUM MENIKAH', 'Belum Menikah'),
        ('MENIKAH', 'Menikah'),
        ('JANDA', 'Janda'),
        ('DUDHA', 'Dudha'),
        ('JOMBLO', 'Jomblo')
    ], string="Status Pernikahan")
    agama = fields.Char(string="Agama")
    tgl_daftar = fields.Date(string="Tanggal Daftar", required=True)  # Penting untuk administrasi
    # no_tlp = fields.Char(string="Nomor Telepon", required=True)  # Penting untuk kontak
    umur = fields.Char(string="Umur", required=True)
    pnd = fields.Selection([
        ('TS', 'Tidak Sekolah'),
        ('TK', 'Taman Kanak-Kanak'),
        ('SD', 'Sekolah Dasar'),
        ('SMP', 'Sekolah Menengah Pertama'),
        ('SMA', 'Sekolah Menengah Atas'),
        ('SLTA/SEDERAJAT', 'SLTA/Sederajat'),
        ('D1', 'Diploma 1'),
        ('D2', 'Diploma 2'),
        ('D3', 'Diploma 3'),
        ('D4', 'Diploma 4'),
        ('S1', 'Sarjana 1'),
        ('S2', 'Sarjana 2'),
        ('S3', 'Sarjana 3'),
        ('-', 'Tidak Diketahui')
    ], string="Pendidikan")
    keluarga = fields.Selection([
        ('AYAH', 'Ayah'),
        ('IBU', 'Ibu'),
        ('ISTRI', 'Istri'),
        ('SUAMI', 'Suami'),
        ('SAUDARA', 'Saudara'),
        ('ANAK', 'Anak')
    ], string="Hubungan Keluarga")
    namakeluarga = fields.Char(string="Nama Keluarga")  # Tidak semua pasien punya keluarga dekat
    kd_pj = fields.Many2one('cdn.penanggung_jawab',string="Kode Penjamin")  # Bisa bayar sendiri
    no_peserta = fields.Char(string="Nomor Peserta")
    kd_kel = fields.Char(string="Kode Kelurahan", required=True)
    kd_kec = fields.Many2one('cdn.ref_kecamatan', string="Kecamatan", required=True)
    kd_kab = fields.Many2one('cdn.ref_kota', string="Kabupaten/Kota", required=True)
    pekerjaanpj = fields.Char(string="Pekerjaan Penjamin")
    alamatpj = fields.Text(string="Alamat Penjamin")
    kelurahanpj = fields.Char(string="Kelurahan Penjamin")
    kecamatanpj = fields.Many2one('cdn.ref_kecamatan', string="Kecamatan Penjamin")
    kabupatenpj = fields.Many2one('cdn.ref_kota',string="Kabupaten Penjamin")
    perusahaan_pasien = fields.Many2one('cdn.perusahaan_pasien', string="Perusahaan Pasien")
    suku_bangsa = fields.Many2one('cdn.suku', string="Suku Bangsa")
    bahasa_pasien = fields.Many2one('res.lang', string="Bahasa Pasien")
    cacat_fisik = fields.Many2one('cdn.cacat_fisik', string="Cacat Fisik")
    # email = fields.Char(string="Email")
    nip = fields.Char(string="NIP")
    kd_prop = fields.Many2one('cdn.ref_propinsi', string="Provinsi", required=True)
    propinsipj = fields.Many2one('cdn.ref_propinsi', string="Propinsi Penjamin")

    @api.model
    def action_activate_account(self):
        """Metode untuk mengaktifkan akun pasien."""
        for record in self:
            record.is_active = True
        return True

    @api.model
    def create(self, vals):
        if vals.get('no_rkm_medis', 'Baru') == 'Baru':
            current_year = datetime.now().year
            last_record = self.search([('no_rkm_medis', 'like', f'KMR/{current_year}/%')], order='id desc', limit=1)

            if last_record:
                last_id = last_record.no_rkm_medis
                try:
                    last_number = int(last_id.split('/')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1

            vals['no_rkm_medis'] = f'KMR/{current_year}/{new_number:03d}'
        return super(Pasien, self).create(vals)