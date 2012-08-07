# -*- coding: utf-8 -*-

from osv import osv, fields

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _name = _inherit 
    
    def _wlog_single_production_ids_raw(self, cr, uid, ids, field_name, arg, context):
        """ return, without loss of generality, the first of production_ids as single name
            in most cases, it will be only one item there, anyway (as business logic creates only one) """
        res = {}
        for pck in self.browse(cr, uid, ids):
            
            if not pck.production_ids_raw:
                res[pck.id] = None
                continue
            
            res[pck.id] = pck.production_ids_raw[0].name or None
            
        return res
    
    _columns = {
        'production_ids_raw': fields.one2many('mrp.production', 'picking_id',
                                          string="Production orders",
                                          help="Production orders this picking provides raw material for"),
        "production_ids_raw_single": fields.function(_wlog_single_production_ids_raw, 
                                         type='char', size=64, method=True,
                                         string="Production order",
                                         help="Production order this move provides raw material for"),
    }

stock_picking()


class stock_move(osv.osv):
    _inherit = "stock.move"
    _name = _inherit 
    
    _columns = {
        'production_ids_raw': fields.related('picking_id','production_ids_raw',
                                         type="one2many", relation="mrp.production", 
                                          string="Production orders",
                                          help="Production orders this picking provides raw material for"),

        'production_ids_raw_single': fields.related('picking_id','production_ids_raw_single',
                                         type="char", size="64", 
                                         string="Production order",
                                         help="Production order this move provides raw material for"),
    }

stock_move()
