from odoo import models, fields, api

class Pemeriksaan_ralan(models.Model):
    _name = 'cdn.pemeriksaan_ralan'
    _description = 'Pemeriksaan Rawat Jalan'
    _rec_name = 'no_rawat'

    no_rawat = fields.Char(string='No Rawat', required=True, index=True)
    tgl_perawatan = fields.Date(string='Tanggal Perawatan', required=True)
    jam_rawat = fields.Float(string='Jam Rawat', required=True, help="Gunakan format jam desimal (contoh: 14.30 untuk 14:30)")
    suhu_tubuh = fields.Char(string='Suhu Tubuh', size=5)
    tensi = fields.Char(string='Tensi', size=8, required=True)
    nadi = fields.Char(string='Nadi', size=3)
    respirasi = fields.Char(string='Respirasi', size=3)
    tinggi = fields.Char(string='Tinggi', size=5)
    berat = fields.Char(string='Berat', size=5)
    spo2 = fields.Char(string='SPO2', size=3, required=True)
    gcs = fields.Char(string='GCS', size=10)
    kesadaran = fields.Selection([
        ('Compos Mentis', 'Compos Mentis'),
        ('Somnolence', 'Somnolence'),
        ('Sopor', 'Sopor'),
        ('Coma', 'Coma'),
        ('Alert', 'Alert'),
        ('Confusion', 'Confusion'),
        ('Voice', 'Voice'),
        ('Pain', 'Pain'),
        ('Unresponsive', 'Unresponsive'),
        ('Apatis', 'Apatis'),
        ('Delirium', 'Delirium'),
    ], string='Kesadaran', required=True)
    keluhan = fields.Text(string='Keluhan', size=2000)
    pemeriksaan = fields.Text(string='Pemeriksaan', size=2000)
    alergi = fields.Char(string='Alergi', size=80)
    lingkar_perut = fields.Char(string='Lingkar Perut', size=5)
    rtl = fields.Text(string='RTL', required=True, size=2000)
    penilaian = fields.Text(string='Penilaian', required=True, size=2000)
    instruksi = fields.Text(string='Instruksi', required=True, size=2000)
    evaluasi = fields.Text(string='Evaluasi', required=True, size=2000)
    nip = fields.Char(string='NIP', required=True, index=True)

    _sql_constraints = [
        ('pemeriksaan_ralan_uniq', 'unique(no_rawat, tgl_perawatan, jam_rawat)', 'Kombinasi No Rawat, Tanggal Perawatan, dan Jam Rawat harus unik!')
    ]

    @api.constrains('suhu_tubuh', 'tensi', 'nadi', 'respirasi', 'tinggi', 'berat', 'spo2', 'gcs', 'lingkar_perut')
    def _check_field_constraints(self):
        for record in self:
            if record.suhu_tubuh and not record.suhu_tubuh.replace('.', '').isdigit():
                raise ValidationError("Suhu Tubuh harus berupa angka valid.")
            if record.tensi and not record.tensi.replace('/', '').isdigit():
                raise ValidationError("Tensi harus berupa angka valid dengan format '120/80'.")
            if record.nadi and not record.nadi.isdigit():
                raise ValidationError("Nadi harus berupa angka.")
            if record.respirasi and not record.respirasi.isdigit():
                raise ValidationError("Respirasi harus berupa angka.")
            if record.tinggi and not record.tinggi.isdigit():
                raise ValidationError("Tinggi harus berupa angka.")
            if record.berat and not record.berat.isdigit():
                raise ValidationError("Berat harus berupa angka.")
            if record.spo2 and not record.spo2.isdigit():
                raise ValidationError("SPO2 harus berupa angka.")
            if record.lingkar_perut and not record.lingkar_perut.isdigit():
                raise ValidationError("Lingkar Perut harus berupa angka.")

    @api.model
    def create(self, vals):
        # Logika tambahan jika diperlukan saat membuat record baru
        return super(PemeriksaanRalan, self).create(vals)

    def write(self, vals):
        # Logika tambahan jika diperlukan saat mengupdate record
        return super(PemeriksaanRalan, self).write(vals)