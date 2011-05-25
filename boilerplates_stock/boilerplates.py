# -*- coding: utf-8 -*-

from osv import osv, fields

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"
    _inherit = "boilerplates.text"

    _columns = {
        'usability_stock': fields.boolean("Usable for Stock"),
    }
    _defaults = {
        "usability_stock": lambda *a: True,
    }
boilerplates_text()
