# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_picking_clientorderref(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    def _get_sale_client_order_ref(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for session in self.browse(cr,uid,ids,context=context):
            if (session.sale_id):
                res[session.id] = session.sale_id.client_order_ref or False
        return res

    def _trigger_sale_client_order_ref(self, cr, uid, ids, context={}):
        return self.search(cr, uid, [('sale_id','in',ids)])
        
    
    _columns = {
        "sale_client_order_ref": fields.function(_get_sale_client_order_ref, type='char', size=64,
                                                 method=True, string="Sales Order Customer Reference", 
                                                 store={'sale.order':(_trigger_sale_client_order_ref,['client_order_ref'],10)})
    }
    
stock_picking_clientorderref()
