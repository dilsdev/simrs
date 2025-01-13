from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class Pasien(models.Model):
    _name = 'cdn.pasien'
    _description = 'Data Pasien'
    _inherits = {'res.partner': 'partner_id'}
    # Field Definitions
    no_rkm_medis = fields.Char(string='No Rekam Medis', required=True, copy=False, readonly=True, default='NRM/20XX/XXX')
    partner_id = fields.Many2one('res.partner', string="Contact", required=False, ondelete="cascade")
    no_ktp = fields.Char(string="Nomor KTP", required=True)
    jk = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], string="Jenis Kelamin", required=True)
    tmp_lahir = fields.Char(string="Tempat Lahir", required=True)
    tgl_lahir = fields.Date(string="Tanggal Lahir", required=True)
    p_jawab = fields.Char(string="Nama PJ")
    alamat = fields.Text(string="Alamat", required=True)
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
    tgl_daftar = fields.Date(string="Tanggal Daftar", required=True)
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
    namakeluarga = fields.Char(string="Nama Keluarga")
    kd_pj = fields.Many2one('cdn.penanggung_jawab', string="Kode Penjamin")
    no_peserta = fields.Char(string="Nomor Peserta")
    kd_kel = fields.Char(string="Kode Kelurahan", required=True)
    kd_kec = fields.Many2one('cdn.ref_kecamatan', string="Kecamatan", ondelete="set null")
    kd_kab = fields.Many2one('cdn.ref_kota', string="Kabupaten/Kota", ondelete="set null")
    kd_prop = fields.Many2one('cdn.ref_propinsi', string="Provinsi", ondelete="set null")
    pekerjaanpj = fields.Char(string="Pekerjaan Penjamin")
    alamatpj = fields.Text(string="Alamat Penjamin")
    kelurahanpj = fields.Char(string="Kelurahan Penjamin")
    kecamatanpj = fields.Many2one('cdn.ref_kecamatan', string="Kecamatan Penjamin")
    kabupatenpj = fields.Many2one('cdn.ref_kota', string="Kabupaten Penjamin")
    perusahaan_pasien = fields.Many2one('cdn.perusahaan_pasien', string="Perusahaan Pasien")
    suku_bangsa = fields.Many2one('cdn.suku', string="Suku Bangsa")
    bahasa_pasien = fields.Many2one('res.lang', string="Bahasa Pasien")
    cacat_fisik = fields.Many2one('cdn.cacat_fisik', string="Cacat Fisik")
    nip = fields.Char(string="NIP")
    propinsipj = fields.Many2one('cdn.ref_propinsi', string="Propinsi Penjamin")

    # Methods
    @api.model
    def action_activate_account(self):
        """Metode untuk mengaktifkan akun pasien."""
        for record in self:
            record.is_active = True
        return True

    @api.model
    def create(self, vals):
        _logger.debug("Creating Pasien with values: %s", vals)
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

        self._validate_many2one_fields(vals)
        return super(Pasien, self).create(vals)

    def write(self, vals):
        _logger.debug("Updating Pasien ID %s with values: %s", self.ids, vals)
        self._validate_many2one_fields(vals)
        return super(Pasien, self).write(vals)

    def _validate_many2one_fields(self, vals):
        many2one_fields = ['kd_kec', 'kd_kab', 'kd_prop']
        for field in many2one_fields:
            if field in vals and vals[field]:
                record = self.env[self._fields[field].comodel_name].browse(vals[field])
                if not record.exists():
                    _logger.error("Invalid reference for field %s: %s", field, vals[field])
                    raise ValueError(f"Invalid reference for field {field}: {vals[field]}")

    @api.onchange('kd_kec', 'kd_kab', 'kd_prop')
    def _onchange_location(self):
        for record in self:
            _logger.debug(
                "Onchange triggered for record ID %s: kd_kec=%s, kd_kab=%s, kd_prop=%s",
                record.id, record.kd_kec, record.kd_kab, record.kd_prop
            )
            if record.kd_kec and not record.kd_kec.exists():
                _logger.warning("Invalid kd_kec reference for record ID %s", record.id)
                record.kd_kec = False
            if record.kd_kab and not record.kd_kab.exists():
                _logger.warning("Invalid kd_kab reference for record ID %s", record.id)
                record.kd_kab = False
            if record.kd_prop and not record.kd_prop.exists():
                _logger.warning("Invalid kd_prop reference for record ID %s", record.id)
                record.kd_prop = False
