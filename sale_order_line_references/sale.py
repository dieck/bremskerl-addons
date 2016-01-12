# -*- coding: utf-8 -*-

from osv import osv, fields

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _name = _inherit 
    
    _columns = {
        'client_order_ref': fields.related('order_id', 'client_order_ref', type='char', string='Cust. Ref.'),
    }

sale_order_line()
