# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Aturan_pemakaian(models.Model):
    _name = 'cdn.aturan_pemakaian'
    _description = 'Kategori Perawatan'

    name= fields.Char(string='Aturan Pemakaian', required=True)
