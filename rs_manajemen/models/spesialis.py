# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Spesialis(models.Model):
    _name = 'cdn.spesialis'
    _description = 'Spesialis'

    kode= fields.Char(string='Kode', required=True)
    name= fields.Char(string='Spesialis', required=True)
