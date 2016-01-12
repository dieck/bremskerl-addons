# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"

    _columns = {
        'premerge_sale_client_order_ref': fields.related('premerge_sale_id', 'client_order_ref', type='char', size=64, string='Pre-Merge Sales Order Customer Reference'),
    }
        
stock_move()
