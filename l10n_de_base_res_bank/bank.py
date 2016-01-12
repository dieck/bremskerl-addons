# -*- coding: UTF-8 -*-
'''
@author: Marco Dieckhoff
'''

from osv import osv, fields

class l10n_de_base_res_bank(osv.osv):
    _name = 'res.bank'
    _inherit = 'res.bank'
    _columns = {
        "bic_de": fields.integer("German BIC", size=64, help="German Bank Identifier Code (Bankleitzahl)"),
    }
l10n_de_base_res_bank()
