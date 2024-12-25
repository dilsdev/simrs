from odoo import models, fields, api

class IPDTreatment(models.Model):
    _name = 'cdn.ipd.treatment'
    _description = 'Jenis Perawatan Rawat Inap'
    _rec_name = 'name'

    code = fields.Char(string='Kode Perawatan', readonly=True, copy=False, default='New')
    name = fields.Char(string='Nama Jenis Perawatan', required=True)
    category_id = fields.Many2one('product.category', string='Kategori', required=True)
    doctor_fee = fields.Float(string='Tarif Dokter', required=True)
    nurse_fee = fields.Float(string='Tarif Perawat', required=True)
    room_fee = fields.Float(string='Tarif Kamar', compute='_compute_room_fee', store=True, readonly=True)
    total_fee = fields.Float(string='Total Tarif', compute='_compute_total_fee', store=True)
    penjab_id = fields.Many2one('cdn.penanggung_jawab', string='Penanggung Jawab', required=True)
    bangsal_id = fields.Many2one('cdn.bangsal', string='Bangsal', required=True)
    kelas_kamar = fields.Selection(
        selection=[
            ('kelas_1', 'Kelas 1'), ('kelas_2', 'Kelas 2'), ('kelas_3', 'Kelas 3'),
            ('kelas_utama', 'Kelas Utama'), ('kelas_vip', 'Kelas VIP'), ('kelas_vvip', 'Kelas VVIP')
        ],
        string='Kelas Kamar',
        required=True
    )
    status = fields.Boolean(string='Status', default=True)
    product_id = fields.Many2one('product.product', string="Produk Layanan", readonly=True)
    tax_id = fields.Many2one('account.tax', string='Jenis Pajak', domain=[('type_tax_use', '=', 'sale')])
    total_with_tax = fields.Float(string='Total dengan Pajak', compute='_compute_total_with_tax', store=True)

    @api.depends('bangsal_id', 'kelas_kamar')
    def _compute_room_fee(self):
        for rec in self:
            if rec.kelas_kamar and rec.bangsal_id:
                kamar = self.env['cdn.kamar'].search([
                    ('bangsal_id', '=', rec.bangsal_id.id),
                    ('kelas', '=', rec.kelas_kamar),
                    ('status_data', '=', 'aktif')
                ], limit=1)
                rec.room_fee = kamar.tarif if kamar else 0.0
            else:
                rec.room_fee = 0.0

    @api.depends('doctor_fee', 'nurse_fee', 'room_fee')
    def _compute_total_fee(self):
        for rec in self:
            rec.total_fee = rec.doctor_fee + rec.nurse_fee + rec.room_fee

    @api.depends('total_fee', 'tax_id')
    def _compute_total_with_tax(self):
        for rec in self:
            if rec.tax_id:
                tax_amount = rec.tax_id.amount * rec.total_fee / 100
                rec.total_with_tax = rec.total_fee + tax_amount
            else:
                rec.total_with_tax = rec.total_fee

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_record = self.search([], order='id desc', limit=1)
            if last_record and last_record.code:
                try:
                    last_number = int(last_record.code.split('RI')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            vals['code'] = f'RI{new_number:03d}'

        product = self.env['product.product'].create({
            'name': vals.get('name'),
            'default_code': vals['code'],
            'type': 'service',
            'categ_id': vals.get('category_id'),
            'list_price': vals.get('doctor_fee') + vals.get('nurse_fee') + vals.get('room_fee', 0.0),
            'sale_ok': True,
            'purchase_ok': False,
            'available_in_pos': False,
            'taxes_id': vals.get('taxes_id', []),
        })
        vals['product_id'] = product.id

        return super(IPDTreatment, self).create(vals)