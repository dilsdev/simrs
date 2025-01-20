from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
class RegPeriksa(models.Model):
    _name = 'cdn.reg_periksa'
    _description = 'Registrasi Pemeriksaan'
    _rec_name = 'no_rawat'

    no_reg = fields.Char(string='No Registrasi', required=False) 
    no_rawat = fields.Char(string='No Rawat', required=True, copy=False, readonly=True, default=f'RW/{datetime.now().year}/XXXX', index=True)
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
            self.kd_poli = self.no_rkm_medis.kd_poli or ''
        else:
            self.p_jawab = ''
            self.hubunganpj = ''
            self.almt_pj = ''
            self.kd_poli = ''

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

    def write(self, vals):
        # Panggil write asli terlebih dahulu
        result = super(RegPeriksa, self).write(vals)
        
        # Update record terkait di rawat_jalan
        for record in self:
            rawat_jalan = self.env['cdn.rawat_jalan'].search([
                ('no_rawat', '=', record.no_rawat)
            ], limit=1)
            
            if rawat_jalan:
                rawat_jalan_vals = {
                    'id_reg_periksa': record.id,
                    'kd_dokter': record.kd_dokter.id if record.kd_dokter else False,
                    'no_rkm_medis': record.no_rkm_medis.id if record.no_rkm_medis else False,
                    'pasien': record.no_rkm_medis.name if record.no_rkm_medis else False,
                    'kd_poli': record.kd_poli.id if record.kd_poli else False,
                }
                try:
                    rawat_jalan.write(rawat_jalan_vals)
                except Exception as e:
                    _logger.error(f"Error updating rawat_jalan record: {str(e)}")
                    raise
        
        return result

    def unlink(self):
        # Hapus record terkait di rawat_jalan sebelum menghapus reg_periksa
        for record in self:
            rawat_jalan = self.env['cdn.rawat_jalan'].search([
                ('no_rawat', '=', record.no_rawat)
            ])
            if rawat_jalan:
                try:
                    rawat_jalan.unlink()
                except Exception as e:
                    _logger.error(f"Error deleting rawat_jalan record: {str(e)}")
                    raise
        
        # Setelah itu baru hapus record reg_periksa
        return super(RegPeriksa, self).unlink()

    @api.model
    def create(self, vals):
        # Generate no_rawat first
        year_short = datetime.now().year
        
        # Create temporary record to get ID
        temp_record = super(RegPeriksa, self).create(vals)
        record_id = f'{temp_record.id:05d}'
        no_rawat = f'RWT/{year_short}/{record_id}'
        
        # Update the record with final no_rawat
        temp_record.write({'no_rawat': no_rawat})
        
        # Create rawat_jalan record AFTER reg_periksa is fully created
        if temp_record.id:
            try:
                self.env['cdn.rawat_jalan'].create({
                    'id_reg_periksa': temp_record.id,
                    'no_rawat': no_rawat,
                    'kd_dokter': temp_record.kd_dokter.id if temp_record.kd_dokter else False,
                    'no_rkm_medis': temp_record.no_rkm_medis.id if temp_record.no_rkm_medis else False,
                    'pasien': temp_record.no_rkm_medis.name if temp_record.no_rkm_medis else False,
                    'kd_poli': temp_record.kd_poli.id if temp_record.kd_poli else False,
                })
            except Exception as e:
                _logger.error(f"Error creating rawat_jalan record: {str(e)}")
                raise

        return temp_record