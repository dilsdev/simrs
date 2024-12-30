from odoo import api, fields, models
from odoo.exceptions import UserError

class Petugas(models.Model):
    _name = 'cdn.petugas'
    _description = 'Data Petugas Rumah Sakit'
    _inherits = {'hr.employee': 'employee_id'}

    employee_id = fields.Many2one(
        'hr.employee', 
        required=True, 
        ondelete='cascade', 
        string='Employee'
    )

    # Informasi Pegawai
    nip = fields.Char(string="NIP")
    jk = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], string='Jenis Kelamin')
    tmp_lahir = fields.Char('Tempat Lahir')
    tgl_lahir = fields.Date('Tanggal Lahir')
    gol_drh = fields.Selection([('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB'), ('-', 'Tidak Diketahui')], string='Golongan Darah')
    agama = fields.Char('Agama')
    almt_tgl = fields.Char('Alamat dan Tanggal')
    no_telp = fields.Char('Nomor Telepon')
    stts_nikah = fields.Selection([
        ('BELUM MENIKAH', 'Belum Menikah'),
        ('MENIKAH', 'Menikah'),
        ('JANDA', 'Janda'),
        ('DUDHA', 'Duda'),
        ('JOMBLO', 'Jomblo')
    ], string='Status Pernikahan')
    status = fields.Selection([('0', 'Non-Aktif'), ('1', 'Aktif')], string='Status', default='1')
    jabatan_id = fields.Many2one('cdn.jabatan', string="Jabatan", help="Jabatan Petugas")

    # Jenis Pegawai (Employee Type)
    jns_pegawai = fields.Selection([
        ('dokter', 'Dokter'),
        ('perawat', 'Perawat'),
        ('apoteker', 'Apoteker'),
        ('tenaga_medis_lainnya', 'Tenaga Medis Lainnya'),
        ('administrasi_rumah_sakit', 'Administrasi Rumah Sakit'),
        ('petugas_kebersihan_keamanan', 'Petugas Kebersihan dan Keamanan'),
        ('teknisi_medis', 'Teknisi Medis'),
        ('manajer_rumah_sakit', 'Manajer Rumah Sakit'),
        ('staf_keuangan_akuntansi', 'Staf Keuangan dan Akuntansi'),
        ('staf_it', 'Staf IT'),
    ], string=' Jenis Pegawai', required=True)

    def activate_account(self):
        self.ensure_one()
        if not self.employee_id.work_email:
            raise UserError("Email tidak ditemukan di data karyawan.")
        
        user = self.env['res.users'].search([('login', '=', self.employee_id.work_email)], limit=1)
        
        if not user:
            raise UserError(f"User  dengan email {self.employee_id.work_email} tidak ditemukan.")
        
        # Menentukan group yang sesuai berdasarkan jenis pegawai
        group_mapping = {
            'dokter': 'rs_dokter.group_dokter_staff',
            'perawat': 'rs_perawat.group_perawat_staff',
            'apoteker': 'rs_apoteker.group_apoteker_staff',
            'tenaga_medis_lainnya': 'rs_tenaga_medis_lainnya.group_tenaga_medis_lainnya',
            'administrasi_rumah_sakit': 'rs_administrasi_rumah_sakit.group_administrasi_staff',
            'petugas_kebersihan_keamanan': 'rs_petugas_kebersihan_keamanan.group_petugas_kebersihan_keamanan',
            'teknisi_medis': 'rs_teknisi_medis.group_teknisi_medis',
            'manajer_rumah_sakit': 'rs_manajer_rumah_sakit.group_manajer_rumah_sakit',
            'staf_keuangan_akuntansi': 'rs_staf_keuangan_akuntansi.group_staf_keuangan_akuntansi',
            'staf_it': 'rs_staf_it.group_staf_it'
        }

        if self.jns_pegawai not in group_mapping:
            raise UserError("Jenis pegawai tidak terdaftar untuk penambahan group.")

        group = self.env.ref(group_mapping[self.jns_pegawai])
        if group not in user.groups_id:
            user.write({'groups_id': [(4, group.id)]})

        return {
            'type': 'ir.actions.act_window',
            'name': 'User ',
            'res_model': 'res.users',
            'res_id': user.id,
            'view_mode': 'form',
            'target': 'current',
        }