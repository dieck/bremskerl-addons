# -*- coding: utf-8 -*-

from osv import fields, osv

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_related_picking_ids(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        stock_move = self.pool.get("stock.move")
        
        for record in self.browse(cr, uid, ids, context=context):
            pickings = {}
            for ol in record.order_line:
                for m in ol.move_ids:
                    if (m.picking_id):
                        pickings[m.picking_id.id] = True
            
            
            premerge_ids = stock_move.search(cr, uid, [('premerge_sale_id','=',record.id)], context=context)
            for p in stock_move.browse(cr,uid,premerge_ids,context=context):
                if (p.picking_id.id):
                    pickings[p.picking_id.id] = True
                
            result[record.id] = pickings.keys()
        return result

    _columns = {
        'related_picking_ids': fields.function(_get_related_picking_ids, method=True, type='many2many', relation="stock.picking", string="Related Pickings"),
    }
        
sale_order()



