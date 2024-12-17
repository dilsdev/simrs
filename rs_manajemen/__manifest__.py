# -*- coding: utf-8 -*-
{
    'name': "RS Manajemen",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',


        # Master Data
        'views/menu.xml',
        'views/bangsal.xml',
        'views/kamar.xml',
        'views/poliklinik.xml',
        'views/res_lang.xml',
        'views/cacat_fisik.xml',
        'views/perusahaan_pasien.xml',
        'views/suku.xml',
        'views/ref_kecamatan.xml',
        'views/ref_kota.xml',
        'views/ref_provinsi.xml',
        'views/ref_desa.xml',
        'views/penanggung_jawab.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'sequence': -10,
    'application': True,
}

