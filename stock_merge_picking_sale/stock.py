# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name
   
    _columns = {
        'premerge_sale_id': fields.many2one('sale.order', 'Pre-Merge Sales Order Reference'),
    }
        
stock_move()
