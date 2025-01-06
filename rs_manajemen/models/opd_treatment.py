from odoo import models, fields, api
from datetime import datetime

class OPDTreatment(models.Model):
    _name = 'cdn.opd.treatment'
    _description = 'Jenis Perawatan Rawat Jalan'
    _rec_name = 'name'

    # Kode Perawatan (Auto-generated)
    code = fields.Char(string='Kode Perawatan', readonly=True, copy=False, default='RJXXX')

    # Nama Jenis Perawatan
    name = fields.Char(string='Nama Jenis Perawatan', required=True)

    # Kategori Product
    category_id = fields.Many2one('product.category', string='Kategori', required=True)

    # Tarif Dokter & Perawat
    doctor_fee = fields.Float(string='Tarif Dokter', required=True)
    nurse_fee = fields.Float(string='Tarif Perawat', required=True)
    total_fee = fields.Float(string='Total Tarif', compute='_compute_total_fee', store=True)

    # Penanggung Jawab dan Poliklinik
    penjab_id = fields.Many2one('cdn.penanggung_jawab', string='Penanggung Jawab', required=True)
    poliklinik_id = fields.Many2one('cdn.poliklinik', string='Poliklinik', required=True)

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')],
        string='State',
        default='draft'
    )

    # Produk yang Terhubung
    product_id = fields.Many2one('product.product', string="Produk Layanan", readonly=True)

    # Pajak yang Terhubung
    taxes_id = fields.Many2many('account.tax', string='Pajak', related='product_id.taxes_id', readonly=True)
    tax_id = fields.Many2one('account.tax', string='Jenis Pajak', domain=[('type_tax_use', '=', 'sale')])

    # Total setelah pajak
    total_with_tax = fields.Float(string='Total dengan Pajak', compute='_compute_total_with_tax', store=True)

    # Compute Total Tarif
    @api.depends('doctor_fee', 'nurse_fee')
    def _compute_total_fee(self):
        for rec in self:
            rec.total_fee = rec.doctor_fee + rec.nurse_fee

    # Compute Total dengan Pajak
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
                    last_number = int(last_record.code.split('RJ')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            vals['code'] = f'RJ{new_number:03d}'

        product = self.env['product.product'].create({
            'name': vals.get('name'),
            'default_code': vals['code'],
            'type': 'service',
            'categ_id': vals.get('category_id'),
            'list_price': vals.get('doctor_fee') + vals.get('nurse_fee') + vals.get('room_fee', 0.0),
            'sale_ok': vals.get('state') == 'confirmed',
            'purchase_ok': False,
            'available_in_pos': False,
            'taxes_id': vals.get('taxes_id', []),
        })
        vals['product_id'] = product.id

        return super(OPDTreatment, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
            if rec.product_id:
                rec.product_id.write({'sale_ok': True})

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            if rec.product_id:
                rec.product_id.write({'sale_ok': False})