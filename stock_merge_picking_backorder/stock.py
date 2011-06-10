# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"

    _columns = {
        'premerge_backorder_id': fields.many2one('stock.picking', 'Pre-Merge Back Order')
    }
        
stock_move()
