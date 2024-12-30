from odoo import models, fields, api
from datetime import datetime
class Pasien(models.Model):
    _name = 'cdn.pasien'
    _description = 'Data Pasien'
    _inherits = {'res.partner': 'partner_id'}

    no_rkm_medis = fields.Char(string='No Rekam Medis', required=True, copy=False, readonly=True, default='NRM/20XX/XXX')
    nm_pasien = fields.Char(string="Nama Pasien")
    partner_id = fields.Many2one('res.partner', string="Contact", required=True, ondelete="cascade")
    no_ktp = fields.Char(string="Nomor KTP")
    jk = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], string="Jenis Kelamin")
    tmp_lahir = fields.Char(string="Tempat Lahir")
    tgl_lahir = fields.Date(string="Tanggal Lahir")
    nm_ibu = fields.Char(string="Nama Ibu", required=True)
    alamat = fields.Text(string="Alamat")
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
    tgl_daftar = fields.Date(string="Tanggal Daftar")
    no_tlp = fields.Char(string="Nomor Telepon")
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
    ], string="Pendidikan", required=True)
    keluarga = fields.Selection([
        ('AYAH', 'Ayah'),
        ('IBU', 'Ibu'),
        ('ISTRI', 'Istri'),
        ('SUAMI', 'Suami'),
        ('SAUDARA', 'Saudara'),
        ('ANAK', 'Anak')
    ], string="Hubungan Keluarga")
    namakeluarga = fields.Char(string="Nama Keluarga", required=True)
    kd_pj = fields.Char(string="Kode Penjamin", required=True)
    no_peserta = fields.Char(string="Nomor Peserta")
    kd_kel = fields.Char(string="Kode Kelurahan", required=True)
    kd_kec = fields.Many2one('cdn.ref_kecamatan', string="Kecamatan", required=True)
    kd_kab = fields.Many2one('cdn.ref_kota', string="Kabupaten/Kota", required=True)
    pekerjaanpj = fields.Char(string="Pekerjaan Penjamin", required=True)
    alamatpj = fields.Text(string="Alamat Penjamin", required=True)
    kelurahanpj = fields.Char(string="Kelurahan Penjamin", required=True)
    kecamatanpj = fields.Char(string="Kecamatan Penjamin", required=True)
    kabupatenpj = fields.Char(string="Kabupaten Penjamin", required=True)
    perusahaan_pasien = fields.Many2one('cdn.perusahaan_pasien', string="Perusahaan Pasien", required=True)
    suku_bangsa = fields.Many2one('cdn.suku', string="Suku Bangsa", required=True)
    bahasa_pasien = fields.Many2one('res.lang', string="Bahasa Pasien", required=True)
    cacat_fisik = fields.Many2one('cdn.cacat_fisik', string="Cacat Fisik", required=True)
    email = fields.Char(string="Email", required=True)
    nip = fields.Char(string="NIP", required=True)
    kd_prop = fields.Many2one('cdn.ref_propinsi', string="Provinsi", required=True)
    propinsipj = fields.Char(string="Propinsi Penjamin", required=True)

    @api.model
    def action_activate_account(self):
        """Metode untuk mengaktifkan akun pasien."""
        # Implementasi logika aktivasi akun
        for record in self:
            # Contoh logika
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