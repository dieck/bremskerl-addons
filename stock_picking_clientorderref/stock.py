# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_picking_clientorderref(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    _columns = {
         'sale_client_order_ref' : fields.related('sale_id', 'client_order_ref', type='char', size=64, string='Sales Order Customer Reference'),
    }
    
stock_picking_clientorderref()
