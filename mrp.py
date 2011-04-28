# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_bom_parentref(osv.osv):
    _name = "mrp.bom"
    _inherit = "mrp.bom"
    
    _columns = {
        'bom_code': fields.related("bom_id", "code", type="char", string="Parent Ref.", readonly=True),
    }
            
mrp_bom_parentref()
