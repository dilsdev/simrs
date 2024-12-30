from odoo import models, fields, api

class LabTreatment(models.Model):
    _name = 'cdn.lab_treatment'
    _description = 'Lab Treatment'
    _rec_name = 'name'

    code = fields.Char(string='Code', readonly=True, copy=False, default='New')
    name = fields.Char(string='Treatment Name', required=True)
    category_id = fields.Many2one('cdn.category', string='Category', required=True)
    doctor_fee = fields.Float(string='Doctor Fee', required=True)
    nurse_fee = fields.Float(string='Nurse Fee', required=True)
    total_fee = fields.Float(string='Total Fee', compute='_compute_total_fee', store=True)
    penjab_id = fields.Many2one('cdn.penjab', string='Penjab', required=True)
    kelas_kamar = fields.Char(string='Room Class', required=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    tax_id = fields.Many2one('account.tax', string='Tax', domain=[('type_tax_use', '=', 'sale')])
    total_with_tax = fields.Float(string='Total with Tax', compute='_compute_total_with_tax', store=True)
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string='Status', default='draft')

    # One2many relation to the Detail Pemeriksaan model
    detail_pemeriksaan_ids = fields.One2many('cdn.detail_pemeriksaan', 'treatment_id', string='Detail Pemeriksaan')

    @api.depends('doctor_fee', 'nurse_fee')
    def _compute_total_fee(self):
        for rec in self:
            rec.total_fee = rec.doctor_fee + rec.nurse_fee

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
                    last_number = int(last_record.code.split('LT')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            vals['code'] = f'LT{new_number:03d}'

        product = self.env['product.product'].create({
            'name': vals.get('name'),
            'default_code': vals['code'],
            'type': 'service',
            'categ_id': vals.get('category_id'),
            'list_price': vals.get('doctor_fee') + vals.get('nurse_fee'),
            'sale_ok': True,
            'purchase_ok': False,
            'available_in_pos': False,
            'taxes_id': [(6, 0, [vals.get('tax_id')])] if vals.get('tax_id') else [],
        })
        vals['product_id'] = product.id

        return super(LabTreatment, self).create(vals)

class DetailPemeriksaan(models.Model):
    _name = 'cdn.detail_pemeriksaan'
    _description = 'Detail Pemeriksaan'

    treatment_id = fields.Many2one('cdn.lab_treatment', string='Lab Treatment', ondelete='cascade')
    nama_pemeriksaan = fields.Char(string='Nama Pemeriksaan', required=True)
    satuan = fields.Char(string='Satuan', required=True)
    nrl_dewasa = fields.Float(string='NRL Dewasa', required=True)
    nrl_anak = fields.Float(string='NRL Anak', required=True)
    nrp_dewasa = fields.Float(string='NRP Dewasa', required=True)
    nrp_anak = fields.Float(string='NRP Anak', required=True)
