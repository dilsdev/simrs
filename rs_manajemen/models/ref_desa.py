from odoo import models, fields
from odoo.exceptions import UserError

class Ref_desa(models.Model):

    _name               = "cdn.ref_desa"
    _description        = "Tabel Data Ref Desa/Kelurahan"

    name                = fields.Char( required=True, string="Nama Desa",  help="")
    keterangan          = fields.Char( string="Keterangan",  help="")


    kecamatan_id        = fields.Many2one(comodel_name="cdn.ref_kecamatan",  string="Kecamatan",  help="")