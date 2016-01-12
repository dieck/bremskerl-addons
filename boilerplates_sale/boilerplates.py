# -*- coding: utf-8 -*-

from osv import osv, fields

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"
    _inherit = "boilerplates.text"

    _columns = {
        'usability_sale': fields.boolean("Usable for Sales"),
    }
    _defaults = {
        "usability_sale": lambda *a: True,
    }
boilerplates_text()
