# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_production_pre(osv.osv):
    # Dummy to have the fields available at new installations.
    # Get KeyError: 'sale_name' and KeyError: 'sale_ref' otherwise
    # Thought having sale_mrp as requirement should do the trick, but does not.
    # Maybe it has to do something with calling the super() functions below
    _inherit = 'mrp.production'
    _name = 'mrp.production'
    
    _columns = {
        'sale_name': fields.char('Sales Name', size=64),
        'sale_ref': fields.char('Sales Reference', size=64),
    }
mrp_production_pre()


class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    _name = 'mrp.production'

    def _ref_calc(self, cr, uid, ids, field_names=None, arg=False, context=None):
        return super(mrp_production, self)._ref_calc(cr=cr, uid=uid, ids=ids, field_names=field_names, arg=arg, context=context)

    def _get_sale_ref(self, cr, uid, ids, field_name=False):
        return super(mrp_production, self)._get_sale_ref(cr=cr, uid=uid, ids=ids, field_name=field_name)

    def _trigger_ref_calc_stockmove(self, cr, uid, ids, field_name=False):
        return self.pool.get('mrp.production').search(cr, uid, [('move_prod_id','in',ids)]) # here it's still simple
    
    def _trigger_ref_calc_saleorderline(self, cr, uid, ids, field_name=False):
        move_ids = self.pool.get('stock.move').search(cr, uid, [('sale_line_id','in',ids)])
        return self.pool.get('mrp.production').search(cr, uid, [('move_prod_id','in',move_ids)])

    def _trigger_ref_calc_saleorder(self, cr, uid, ids, field_name=False):
        sol_ids = self.pool.get('sale.order.line').search(cr, uid, [('order_id','in',ids)])
        move_ids = self.pool.get('stock.move').search(cr, uid, [('sale_line_id','in',sol_ids)])
        return self.pool.get('mrp.production').search(cr, uid, [('move_prod_id','in',move_ids)])
                                       
    _columns = {
        'sale_name': fields.function(_ref_calc, method=True, multi='sale_name', type='char', size=64, string='Sales Name',
                                     store={'stock.move':(_trigger_ref_calc_stockmove,['sale_line_id'],10),
                                            'sale.order.line':(_trigger_ref_calc_saleorderline,['order_id'],15),
                                            'sale.order':(_trigger_ref_calc_saleorder,['client_order_ref'],20)
                                     },
                                     help='Indicate the name of sales order.'),
        'sale_ref': fields.function(_ref_calc, method=True, multi='sale_name', type='char', size=64, string='Sales Reference',
                                     store={'stock.move':(_trigger_ref_calc_stockmove,['sale_line_id'],10),
                                            'sale.order.line':(_trigger_ref_calc_saleorderline,['order_id'],15),
                                            'sale.order':(_trigger_ref_calc_saleorder,['client_order_ref'],20),
                                     },
                                     help='Indicate the Customer Reference from sales order.'),
    }

mrp_production()
