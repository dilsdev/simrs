from odoo import api, fields, models
from odoo.exceptions import UserError

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    kd_dokter = fields.Char('Kode Dokter', required=True)
    jk = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], string='Jenis Kelamin')
    tmp_lahir = fields.Char('Tempat Lahir')
    tgl_lahir = fields.Date('Tanggal Lahir')
    gol_drh = fields.Selection([('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB'), ('-', 'Tidak Diketahui')], string='Golongan Darah')
    agama = fields.Char('Agama')
    almt_tgl = fields.Char('Alamat dan Tanggal')
    no_telp = fields.Char('Nomor Telepon')
    stts_nikah = fields.Selection([('BELUM MENIKAH', 'Belum Menikah'), ('MENIKAH', 'Menikah'), ('JANDA', 'Janda'), ('DUDHA', 'Duda'), ('JOMBLO', 'Jomblo')], string='Status Pernikahan')
    alumni = fields.Char('Alumni')
    no_ijn_praktek = fields.Char('Nomor Izin Praktek')
    status = fields.Selection([('0', 'Non-Aktif'), ('1', 'Aktif')], string='Status', default='1')

    # Relasi ke spesialis
    spesialis_id = fields.Many2one('cdn.spesialis', string="Spesialis", help="Spesialis Dokter")

    # Relasi ke riwayat pendidikan dokter
    pendidikan_dokter_ids = fields.One2many(inverse_name="dokter_id", string="Riwayat Pendidikan Dokter")

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
    ], string='Jenis Pegawai', required=True)

    # Menambahkan password dan role jika diperlukan
    def activate_account(self):
        if not self.work_email:
            raise UserError("Email tidak ditemukan di data karyawan.")
        if not self.kd_dokter:
            raise UserError("Kode Dokter belum diisi.")
        
        # Cari user berdasarkan email dari work_email
        user = self.env['res.users'].search([('login', '=', self.work_email)], limit=1)
        
        if not user:
            raise UserError(f"User dengan email {self.work_email} tidak ditemukan.")
        
        # Menentukan group yang sesuai berdasarkan jenis pegawai
        groups_to_add = []
        
        if self.jns_pegawai == 'dokter':
            groups_to_add.append(self.env.ref('rs_dokter.group_dokter_staff'))
        elif self.jns_pegawai == 'perawat':
            groups_to_add.append(self.env.ref('rs_perawat.group_perawat_staff'))
        elif self.jns_pegawai == 'apoteker':
            groups_to_add.append(self.env.ref('rs_apoteker.group_apoteker_staff'))
        elif self.jns_pegawai == 'tenaga_medis_lainnya':
            groups_to_add.append(self.env.ref('rs_tenaga_medis_lainnya.group_tenaga_medis_lainnya'))
        elif self.jns_pegawai == 'administrasi_rumah_sakit':
            groups_to_add.append(self.env.ref('rs_administrasi_rumah_sakit.group_administrasi_staff'))
        elif self.jns_pegawai == 'petugas_kebersihan_keamanan':
            groups_to_add.append(self.env.ref('rs_petugas_kebersihan_keamanan.group_petugas_kebersihan_keamanan'))
        elif self.jns_pegawai == 'teknisi_medis':
            groups_to_add.append(self.env.ref('rs_teknisi_medis.group_teknisi_medis'))
        elif self.jns_pegawai == 'manajer_rumah_sakit':
            groups_to_add.append(self.env.ref('rs_manajer_rumah_sakit.group_manajer_rumah_sakit'))
        elif self.jns_pegawai == 'staf_keuangan_akuntansi':
            groups_to_add.append(self.env.ref('rs_staf_keuangan_akuntansi.group_staf_keuangan_akuntansi'))
        elif self.jns_pegawai == 'staf_it':
            groups_to_add.append(self.env.ref('rs_staf_it.group_staf_it'))
        
        if not groups_to_add:
            raise UserError("Jenis pegawai tidak terdaftar untuk penambahan group.")
        
        # Menambahkan semua grup yang diperlukan ke user
        for group in groups_to_add:
            if group not in user.groups_id:
                user.groups_id = [(4, group.id)]
        
        # Atur ulang password user dengan format kd_dokter
        new_password = f"{self.kd_dokter[:6]}"  # Gunakan 6 digit pertama kode dokter
        if len(new_password) < 6:
            raise UserError("Kode dokter harus memiliki minimal 6 karakter.")
        user.write({'password': new_password})

        # Arahkan ke form user yang baru saja diperbarui
        return {
            'type': 'ir.actions.act_window',
            'name': 'User',
            'res_model': 'res.users',
            'res_id': user.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

class pendidikan_dokter(models.Model):
    _name = 'edu.dokter'
    _description = 'Riwayat Pendidikan Dokter'

    name = fields.Char(string='Nama Institusi')
    jenjang = fields.Selection([
        ('sd', 'SD/MI'),
        ('smp', 'SMP/MTS'),
        ('sma', 'SMA/MA'),
        ('diploma', 'D1/D2/D3'),
        ('sarjana', 'D4/S1'),
        ('pasca', 'S2/S3'),
        ('lainnya', 'Lainnya/Non Formal')
    ], string='Jenjang Pendidikan')
    fakultas = fields.Char(string='Fakultas/Jurusan')
    gelar = fields.Char(string='Gelar')
    karya_ilmiah = fields.Char(string='Karya Ilmiah (Skripsi/Tesis/Disertasi)')
    lulus = fields.Date(string='Tanggal Lulus')
    dokter_id = fields.Many2one('hr.employee', string="Dokter", help="Relasi ke dokter")
