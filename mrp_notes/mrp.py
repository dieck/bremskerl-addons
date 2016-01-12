# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_bom(osv.osv):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    
    _columns = {
        'note': fields.text("Notes", translate=True),
    }
        
mrp_bom()
    
    
class mrp_production(osv.osv):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    _columns = {
        'note': fields.text("Notes", translate=True),
    }
        
mrp_production()

