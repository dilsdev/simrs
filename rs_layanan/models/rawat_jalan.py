from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class Rawat_jalan(models.Model):
    _name = 'cdn.rawat_jalan'
    _description = 'Rawat Jalan'
    _rec_name = 'no_rawat'

    id_reg_periksa = fields.Many2one('cdn.reg_periksa')
    no_rawat = fields.Char(
        string='No Rawat', 
        ondelete='cascade'
    )
    kd_dokter = fields.Many2one('cdn.doctor', string='Dokter', readonly=True, store=True)
    no_rkm_medis = fields.Many2one('cdn.pasien', string='Rekam Medis', readonly=True, store=True)
    pasien = fields.Char(string='Pasien', readonly=True, store=True)
    kd_poli = fields.Many2one('cdn.poliklinik', string='Kode Poliklinik', ondelete='cascade', index=True)

    # Rawat Jalan DR Fields
    rawat_jl_dr_no_rawat = fields.Char(string='No Rawat', index=True)
    rawat_jl_dr_kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan', index=True)
    rawat_jl_dr_kd_dokter = fields.Many2one('cdn.doctor', string='Kode Dokter', ondelete='cascade', index=True)
    rawat_jl_dr_tgl_perawatan = fields.Date(string='Tanggal Perawatan')
    rawat_jl_dr_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    rawat_jl_dr_material = fields.Float(string='Material')
    rawat_jl_dr_bhp = fields.Float(string='BHP')
    rawat_jl_dr_tarif_tindakandr = fields.Float(string='Tarif Tindakan Dokter')
    rawat_jl_dr_kso = fields.Float(string='KSO')
    rawat_jl_dr_menejemen = fields.Float(string='Manajemen')
    rawat_jl_dr_biaya_rawat = fields.Float(string='Biaya Rawat', compute='_compute_total_biaya_dr', store=True)
    rawat_jl_dr_stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar', default='Belum')

    # Rawat Jalan PR Fields
    rawat_jl_pr_no_rawat = fields.Char(string='No Rawat', index=True)
    rawat_jl_pr_kd_jenis_prw = fields.Many2one('cdn.jns_perawatan', string='Kode Jenis Perawatan', index=True)
    rawat_jl_pr_nip = fields.Char(string='NIP', index=True)
    rawat_jl_pr_tgl_perawatan = fields.Date(string='Tanggal Perawatan')
    rawat_jl_pr_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    rawat_jl_pr_material = fields.Float(string='Material')
    rawat_jl_pr_bhp = fields.Float(string='BHP')
    rawat_jl_pr_tarif_tindakanpr = fields.Float(string='Tarif Tindakan Petugas')
    rawat_jl_pr_kso = fields.Float(string='KSO')
    rawat_jl_pr_menejemen = fields.Float(string='Manajemen')
    rawat_jl_pr_biaya_rawat = fields.Float(string='Biaya Rawat', compute='_compute_total_biaya_pr', store=True)
    rawat_jl_pr_stts_bayar = fields.Selection([
        ('Sudah', 'Sudah'),
        ('Belum', 'Belum'),
        ('Suspen', 'Suspen')
    ], string='Status Bayar', default='Belum')

    # Pemeriksaan Ralan Fields
    pemeriksaan_ralan_no_rawat = fields.Char(string='No Rawat', index=True)
    pemeriksaan_ralan_tgl_perawatan = fields.Date(string='Tanggal Perawatan')
    pemeriksaan_ralan_jam_rawat = fields.Float(string='Jam Rawat', help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    pemeriksaan_ralan_suhu_tubuh = fields.Char(string='Suhu Tubuh', size=5)
    pemeriksaan_ralan_tensi = fields.Char(string='Tensi', size=8)
    pemeriksaan_ralan_nadi = fields.Char(string='Nadi', size=3)
    pemeriksaan_ralan_respirasi = fields.Char(string='Respirasi', size=3)
    pemeriksaan_ralan_tinggi = fields.Char(string='Tinggi', size=5)
    pemeriksaan_ralan_berat = fields.Char(string='Berat', size=5)
    pemeriksaan_ralan_spo2 = fields.Char(string='SPO2', size=3)
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
    ], string='Kesadaran', default='Compos Mentis')
    pemeriksaan_ralan_keluhan = fields.Text(string='Keluhan', size=2000)
    pemeriksaan_ralan_pemeriksaan = fields.Text(string='Pemeriksaan', size=2000)
    pemeriksaan_ralan_alergi = fields.Char(string='Alergi', size=80)
    pemeriksaan_ralan_lingkar_perut = fields.Char(string='Lingkar Perut', size=5)
    pemeriksaan_ralan_rtl = fields.Text(string='RTL', size=2000)
    pemeriksaan_ralan_penilaian = fields.Text(string='Penilaian', size=2000)
    pemeriksaan_ralan_instruksi = fields.Text(string='Instruksi', size=2000)
    pemeriksaan_ralan_evaluasi = fields.Text(string='Evaluasi', size=2000)
    pemeriksaan_ralan_nip = fields.Char(string='NIP', index=True)

    # Diagnosa Fields
    diagnosa_pasien_no_rawat = fields.Char('No Rawat')
    diagnosa_pasien_status = fields.Selection([
        ('Ralan', 'Rawat Jalan'),
        ('Ranap', 'Rawat Inap')
    ], string='Status', default='Ralan')
    diagnosa_pasien_prioritas = fields.Integer('Prioritas', default=1)
    diagnosa_pasien_status_penyakit = fields.Selection([
        ('Lama', 'Lama'),
        ('Baru', 'Baru')
    ], string='Status Penyakit', default='Baru')
    diagnosa_pasien_reg_periksa_id = fields.Many2one('cdn.reg_periksa', string='No Rawat')
    diagnosa_pasien_penyakit_id = fields.Many2many('cdn.penyakit', string='Kode Penyakit')
    
    @api.onchange('id_reg_periksa')
    def _onchange_id_reg_periksa(self):
        for record in self:
            if record.id_reg_periksa:
                record.update({
                    'kd_dokter': record.id_reg_periksa.kd_dokter.id if record.id_reg_periksa.kd_dokter else False,
                    'no_rkm_medis': record.id_reg_periksa.no_rkm_medis.id if record.id_reg_periksa.no_rkm_medis else False,
                    'pasien': record.id_reg_periksa.no_rkm_medis.name if record.id_reg_periksa.no_rkm_medis else False,
                    'diagnosa_pasien_reg_periksa_id': record.id_reg_periksa.id,
                    'diagnosa_pasien_no_rawat': record.no_rawat
            })
    def _sync_related_records(self, vals):
        """Helper method to sync data with related tables"""
        if not self.no_rawat:
            return

        rawat_jl_dr = self.env['cdn.rawat_jl_dr'].search([('no_rawat', '=', self.no_rawat)], limit=1)
        rawat_jl_pr = self.env['cdn.rawat_jl_pr'].search([('no_rawat', '=', self.no_rawat)], limit=1)
        pemeriksaan_ralan = self.env['cdn.pemeriksaan_ralan'].search([('no_rawat', '=', self.no_rawat)], limit=1)
        diagnosa_pasien = self.env['cdn.diagnosa_pasien'].search([('no_rawat', '=', self.no_rawat)], limit=1)

        if any(key.startswith('diagnosa_pasien_') for key in vals):
            # Get reg_periksa_id safely
            reg_periksa_id = False
            if vals.get('diagnosa_pasien_reg_periksa_id'):
                reg_periksa_id = vals['diagnosa_pasien_reg_periksa_id']
            elif self.id_reg_periksa:
                reg_periksa_id = self.id_reg_periksa.id

            # Get status safely
            status = 'Ralan'
            if vals.get('diagnosa_pasien_status'):
                status = vals['diagnosa_pasien_status']
            elif diagnosa_pasien and hasattr(diagnosa_pasien, 'status'):
                status = diagnosa_pasien.status

            # Get prioritas safely
            prioritas = 1
            if vals.get('diagnosa_pasien_prioritas'):
                prioritas = vals['diagnosa_pasien_prioritas']
            elif diagnosa_pasien and hasattr(diagnosa_pasien, 'prioritas'):
                prioritas = diagnosa_pasien.prioritas

            # Get status_penyakit safely
            status_penyakit = 'Baru'
            if vals.get('diagnosa_pasien_status_penyakit'):
                status_penyakit = vals['diagnosa_pasien_status_penyakit']
            elif diagnosa_pasien and hasattr(diagnosa_pasien, 'status_penyakit'):
                status_penyakit = diagnosa_pasien.status_penyakit

            diagnosa_vals = {
                'no_rawat': self.no_rawat,
                'status': status,
                'prioritas': prioritas,
                'status_penyakit': status_penyakit,
                'reg_periksa_id': reg_periksa_id,
                'penyakit_id': [(6, 0, self.diagnosa_pasien_penyakit_id.ids)] if self.diagnosa_pasien_penyakit_id else [(6, 0, [])],
            }

            if diagnosa_pasien:
                diagnosa_pasien.write(diagnosa_vals)
            else:
                self.env['cdn.diagnosa_pasien'].create(diagnosa_vals)


            # Prepare values for rawat_jl_pr
        if any(key.startswith('rawat_jl_pr_') for key in vals):
            pr_vals = {
                'no_rawat': self.no_rawat,
                'kd_jenis_prw': vals.get('rawat_jl_pr_kd_jenis_prw', rawat_jl_pr.kd_jenis_prw.id if rawat_jl_pr else False),
                'nip': vals.get('rawat_jl_pr_nip', rawat_jl_pr.nip if rawat_jl_pr else False),
                'tgl_perawatan': vals.get('rawat_jl_pr_tgl_perawatan', rawat_jl_pr.tgl_perawatan if rawat_jl_pr else False),
                'jam_rawat': vals.get('rawat_jl_pr_jam_rawat', rawat_jl_pr.jam_rawat if rawat_jl_pr else 0.0),
                'material': vals.get('rawat_jl_pr_material', rawat_jl_pr.material if rawat_jl_pr else 0.0),
                'bhp': vals.get('rawat_jl_pr_bhp', rawat_jl_pr.bhp if rawat_jl_pr else 0.0),
                'tarif_tindakanpr': vals.get('rawat_jl_pr_tarif_tindakanpr', rawat_jl_pr.tarif_tindakanpr if rawat_jl_pr else 0.0),
                'kso': vals.get('rawat_jl_pr_kso', rawat_jl_pr.kso if rawat_jl_pr else 0.0),
                'menejemen': vals.get('rawat_jl_pr_menejemen', rawat_jl_pr.menejemen if rawat_jl_pr else 0.0),
                'biaya_rawat': vals.get('rawat_jl_pr_biaya_rawat', rawat_jl_pr.biaya_rawat if rawat_jl_pr else 0.0),
                'stts_bayar': vals.get('rawat_jl_pr_stts_bayar', rawat_jl_pr.stts_bayar if rawat_jl_pr else 'Belum'),
            }
            if rawat_jl_pr:
                rawat_jl_pr.write(pr_vals)
            else:
                self.env['cdn.rawat_jl_pr'].create(pr_vals)

        # Prepare values for pemeriksaan_ralan
        if any(key.startswith('pemeriksaan_ralan_') for key in vals):
            pemeriksaan_vals = {
                'no_rawat': self.no_rawat,
                'tgl_perawatan': vals.get('pemeriksaan_ralan_tgl_perawatan', pemeriksaan_ralan.tgl_perawatan if pemeriksaan_ralan else False),
                'jam_rawat': vals.get('pemeriksaan_ralan_jam_rawat', pemeriksaan_ralan.jam_rawat if pemeriksaan_ralan else 0.0),
                'suhu_tubuh': vals.get('pemeriksaan_ralan_suhu_tubuh', pemeriksaan_ralan.suhu_tubuh if pemeriksaan_ralan else ''),
                'tensi': vals.get('pemeriksaan_ralan_tensi', pemeriksaan_ralan.tensi if pemeriksaan_ralan else ''),
                'nadi': vals.get('pemeriksaan_ralan_nadi', pemeriksaan_ralan.nadi if pemeriksaan_ralan else ''),
                'respirasi': vals.get('pemeriksaan_ralan_respirasi', pemeriksaan_ralan.respirasi if pemeriksaan_ralan else ''),
                'tinggi': vals.get('pemeriksaan_ralan_tinggi', pemeriksaan_ralan.tinggi if pemeriksaan_ralan else ''),
                'berat': vals.get('pemeriksaan_ralan_berat', pemeriksaan_ralan.berat if pemeriksaan_ralan else ''),
                'spo2': vals.get('pemeriksaan_ralan_spo2', pemeriksaan_ralan.spo2 if pemeriksaan_ralan else ''),
                'gcs': vals.get('pemeriksaan_ralan_gcs', pemeriksaan_ralan.gcs if pemeriksaan_ralan else ''),
                'kesadaran': vals.get('pemeriksaan_ralan_kesadaran', pemeriksaan_ralan.kesadaran if pemeriksaan_ralan else 'Compos Mentis'),
                'keluhan': vals.get('pemeriksaan_ralan_keluhan', pemeriksaan_ralan.keluhan if pemeriksaan_ralan else ''),
                'pemeriksaan': vals.get('pemeriksaan_ralan_pemeriksaan', pemeriksaan_ralan.pemeriksaan if pemeriksaan_ralan else ''),
                'alergi': vals.get('pemeriksaan_ralan_alergi', pemeriksaan_ralan.alergi if pemeriksaan_ralan else ''),
                'lingkar_perut': vals.get('pemeriksaan_ralan_lingkar_perut', pemeriksaan_ralan.lingkar_perut if pemeriksaan_ralan else ''),
                'rtl': vals.get('pemeriksaan_ralan_rtl', pemeriksaan_ralan.rtl if pemeriksaan_ralan else ''),
                'penilaian': vals.get('pemeriksaan_ralan_penilaian', pemeriksaan_ralan.penilaian if pemeriksaan_ralan else ''),
                'instruksi': vals.get('pemeriksaan_ralan_instruksi', pemeriksaan_ralan.instruksi if pemeriksaan_ralan else ''),
                'evaluasi': vals.get('pemeriksaan_ralan_evaluasi', pemeriksaan_ralan.evaluasi if pemeriksaan_ralan else ''),
                'nip': vals.get('pemeriksaan_ralan_nip', pemeriksaan_ralan.nip if pemeriksaan_ralan else ''),
            }
            if pemeriksaan_ralan:
                pemeriksaan_ralan.write(pemeriksaan_vals)
            else:
                self.env['cdn.pemeriksaan_ralan'].create(pemeriksaan_vals)

        # Prepare values for diagnosa_pasien
        if any(key.startswith('diagnosa_pasien_') for key in vals):
            diagnosa_vals = {
                'no_rawat': self.no_rawat,
                'status': vals.get('diagnosa_pasien_status', diagnosa_pasien.status if diagnosa_pasien else 'Ralan'),
                'prioritas': vals.get('diagnosa_pasien_prioritas', diagnosa_pasien.prioritas if diagnosa_pasien else 1),
                'status_penyakit': vals.get('diagnosa_pasien_status_penyakit', diagnosa_pasien.status_penyakit if diagnosa_pasien else 'Baru'),
                'reg_periksa_id': self.id_reg_periksa.id,
                'penyakit_id': [(6, 0, self.diagnosa_pasien_penyakit_id.ids)] if self.diagnosa_pasien_penyakit_id else [(6, 0, [])],
            }

            if diagnosa_pasien:
                diagnosa_pasien.write(diagnosa_vals)
            else:
                self.env['cdn.diagnosa_pasien'].create(diagnosa_vals)


    @api.model
    def create(self, vals):
        record = super(Rawat_jalan, self).create(vals)
        record._sync_related_records(vals)
        return record

    def write(self, vals):
        result = super(Rawat_jalan, self).write(vals)
        for record in self:
            record._sync_related_records(vals)
        return result

    # Compute methods should be updated to store values
    @api.depends('rawat_jl_dr_material', 'rawat_jl_dr_bhp', 'rawat_jl_dr_tarif_tindakandr', 
                'rawat_jl_dr_kso', 'rawat_jl_dr_menejemen')
    def _compute_total_biaya_dr(self):
        for record in self:
            biaya = (
                record.rawat_jl_dr_material +
                record.rawat_jl_dr_bhp +
                record.rawat_jl_dr_tarif_tindakandr +
                record.rawat_jl_dr_kso +
                record.rawat_jl_dr_menejemen
            )
            record.write({'rawat_jl_dr_biaya_rawat': biaya})

    @api.depends('rawat_jl_pr_material', 'rawat_jl_pr_bhp', 'rawat_jl_pr_tarif_tindakanpr', 
                'rawat_jl_pr_kso', 'rawat_jl_pr_menejemen')
    def _compute_total_biaya_pr(self):
        for record in self:
            biaya = (
                record.rawat_jl_pr_material +
                record.rawat_jl_pr_bhp +
                record.rawat_jl_pr_tarif_tindakanpr +
                record.rawat_jl_pr_kso +
                record.rawat_jl_pr_menejemen
            )
            record.write({'rawat_jl_pr_biaya_rawat': biaya})

    def unlink(self):
        """Override unlink to handle related records"""
        for record in self:
            # Delete related records
            related_models = [
                'cdn.rawat_jl_dr',
                'cdn.rawat_jl_pr',
                'cdn.pemeriksaan_ralan',
                'cdn.diagnosa_pasien'
            ]
            for model in related_models:
                self.env[model].search([('no_rawat', '=', record.no_rawat)]).unlink()
        return super(Rawat_jalan, self).unlink()
    
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