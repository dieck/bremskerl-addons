# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_move_notes(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
        
    _columns = {
         # store price
         'notes' : fields.char("Notes", size=128, translate=True),
         'prtnotes': fields.char("Printed Notes", size=128, translate=True),
    }
    
stock_move_notes()
