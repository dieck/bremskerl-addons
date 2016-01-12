# -*- coding: utf-8 -*-

from osv import osv, fields

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"
    _inherit = "boilerplates.text"

    _columns = {
        'usability_purchase': fields.boolean("Usable for Purchase"),
    }
    _defaults = {
        "usability_purchase": lambda *a: True,
    }
boilerplates_text()
