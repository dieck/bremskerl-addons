# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name

    _columns = {
        'product_qty_available': fields.related('product_id','qty_available', string='Current stock'), # type='float' 
    }
        
stock_move()
