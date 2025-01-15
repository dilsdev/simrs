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

    # Jenis Pegawai (Employee Type)
    jns_pegawai = fields.Selection([
        ('kasir', 'Kasir'),
        ('dokter', 'Dokter'),
        ('perawat', 'Perawat'),
        ('apoteker', 'Apoteker'),
    ], string=' Jenis Pegawai', required=True)

    def activate_account(self):
        self.ensure_one()
        if not self.employee_id.work_email:
            raise UserError("Email tidak ditemukan di data karyawan.")
        
        user = self.env['res.users'].search([('login', '=', self.employee_id.work_email)], limit=1)
        
        if not user:
            raise UserError(f"User  dengan email {self.employee_id.work_email} tidak ditemukan.")
        
        group_mapping = {
            'dokter': 'rs_dokter.group_dokter_staff',
            'perawat': 'rs_perawat.group_perawat_staff',
            'apoteker': 'rs_apoteker.group_apoteker_staff',
            'kasir': 'rs_kasir.group_kasir_staff'
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