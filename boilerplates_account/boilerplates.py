# -*- coding: utf-8 -*-

from osv import osv, fields

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"
    _inherit = "boilerplates.text"

    _columns = {
        'usability_account': fields.boolean("Usable for Accounting"),
    }
    _defaults = {
        "usability_account": lambda *a: True,
    }
boilerplates_text()
