from odoo import models, fields, api

class LabTreatment(models.Model):
    _name = 'cdn.lab_treatment'
    _description = 'Lab Treatment'
    _rec_name = 'name'
    
    detail_ids = fields.One2many('cdn.lab_treatment_detail', 'lab_treatment_id', string='Detail Pemeriksaan')

    code = fields.Char(string='Code', readonly=True, copy=False, default='LABXXX')
    name = fields.Char(string='Treatment Name', required=True)
    category_id = fields.Many2one('product.category', string='Kategori', required=True)
    doctor_fee = fields.Float(string='Doctor Fee', required=True)
    nurse_fee = fields.Float(string='Nurse Fee', required=True)
    room_fee = fields.Float(string='Tarif Kamar', compute='_compute_room_fee', store=True, readonly=True)
    total_fee = fields.Float(string='Total Fee', compute='_compute_total_fee', store=True)
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
    product_id = fields.Many2one('product.product', string="Produk Layanan", readonly=True)
    tax_id = fields.Many2one('account.tax', string='Jenis Pajak', domain=[('type_tax_use', '=', 'sale')])
    total_with_tax = fields.Float(string='Total dengan Pajak', compute='_compute_total_with_tax', store=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string='Status', default='draft')

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

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            last_record = self.search([], order='id desc', limit=1)
            if last_record and last_record.code:
                try:
                    last_number = int(last_record.code.split('LAB')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            vals['code'] = f'LAB{new_number:03d}'

        # Determine the 'sale_ok' value based on the state
        sale_ok = True if vals.get('state') == 'confirmed' else False
        
        product = self.env['product.product'].create({
            'name': vals.get('name'),
            'default_code': vals['code'],
            'type': 'service',
            'categ_id': vals.get('category_id'),
            'list_price': vals.get('doctor_fee', 0.0) + vals.get('nurse_fee', 0.0),
            'sale_ok': sale_ok,
            'purchase_ok': False,
            'available_in_pos': False,
            'taxes_id': [(6, 0, [vals['tax_id']])] if vals.get('tax_id') else [],
        })
        vals['product_id'] = product.id

        return super(LabTreatment, self).create(vals)
    
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
            # Update product to have sale_ok = True when confirmed
            if rec.product_id:
                rec.product_id.write({'sale_ok': True})

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            # Update product to have sale_ok = False when draft
            if rec.product_id:
                rec.product_id.write({'sale_ok': False})

    @api.onchange('state')
    def _onchange_status(self):
        if self.state == 'confirmed':
            # Additional logic can go here, like disabling the button
            pass

class LabTreatmentDetail(models.Model):
    _name = 'cdn.lab_treatment_detail'
    _description = 'Lab Treatment Detail'
    
    lab_treatment_id = fields.Many2one('cdn.lab_treatment', string='Lab Treatment', ondelete='cascade')
    nama_pemeriksaan = fields.Char(string='Nama Pemeriksaan', required=True)
    satuan = fields.Char(string='Satuan', required=True)
    nrl_dewasa = fields.Float(string='NRL Dewasa', required=True)
    nrl_anak = fields.Float(string='NRL Anak', required=True)
    nrp_dewasa = fields.Float(string='NRP Dewasa', required=True)
    nrp_anak = fields.Float(string='NRP Anak', required=True)
