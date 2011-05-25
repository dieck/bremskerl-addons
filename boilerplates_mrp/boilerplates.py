# -*- coding: utf-8 -*-

from osv import osv, fields

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"
    _inherit = "boilerplates.text"

    _columns = {
        'usability_mrp': fields.boolean("Usable for Manufacturing"),
    }
    _defaults = {
        "usability_mrp": lambda *a: True,
    }
boilerplates_text()
