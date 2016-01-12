# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_picking_clientorderref(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    def _get_sale_client_order_ref(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for session in self.browse(cr,uid,ids,context=context):
            if (session.sale_id):
                res[session.id] = session.sale_id and session.sale_id.client_order_ref or False
        return res


    ##TODO this does not work and you get a "Key error: sale_id".
    ## using store={'sale.order':(_trigger_sale_client_order_ref,['client_order_ref'],10)}
    def DOESNOTWORK_trigger_sale_client_order_ref(self, cr, uid, ids, context={}):
        return self.search(cr, uid, [('sale_id','IN',ids)])
    
    ##TODO this does not work and shows an SQL error, sale_order.sale_id does not exist
    ## but WHY sale_order? self.search should apply to stock.picking here?
    ## using store={'sale.order':(_trigger_sale_client_order_ref,['client_order_ref'],10)}
    def DOESNOTWORKEITHER_trigger_sale_client_order_ref(self, cr, uid, ids, context={}):
        dom = []
        for id in ids:
            dom.append( ('sale_id','=',id) )
        
        # make "or" domain
        for i in range(len(dom)-1):
            dom.insert(0, '|')
                            
        return self.search(cr, uid, dom)

  
    _columns = {
        "sale_client_order_ref": fields.function(_get_sale_client_order_ref, type='char', size=64,
                                                 method=True, string="Sales Order Customer Reference", 
                                                 store=True)
    }
    
stock_picking_clientorderref()
