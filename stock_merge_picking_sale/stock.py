# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name
        
    def _get_sale_details(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        
        for record in self.browse(cr, uid, ids, context=context):
            cor = None
            st = None
            oid = None
            solt = None

            # order to lookup:
            # sale_line_id exists => will not be changed by merges
            # premerge_sale_id exists => use stored information
            # use sale_id in picking
            
            if (record.sale_line_id):
                solt = "Sale Line from Stock Move"
                if (record.sale_line_id.order_id):
                    oid = record.sale_line_id.order_id.id
                    cor = record.sale_line_id.order_id.client_order_ref or False
                    st = record.sale_line_id.order_id.state or False
            else:
                if (record.premerge_sale_id):
                    oid = record.premerge_sale_id.id
                    cor = record.premerge_sale_id.client_order_ref or False
                    st = record.premerge_sale_id.state or False
                    solt = "Pre-Merge stored Sale Order"
                
                else:
                    if (record.picking_id):
                        solt = "Sale Order of Stock Picking"
                        if (record.picking_id.sale_id):
                            oid = record.picking_id.sale_id.id
                            cor = record.picking_id.sale_id.client_order_ref or False
                            st = record.picking_id.sale_id.state or False
            
            result[record.id] = {'sale_lookup_type': solt, 'sale_lookup_order_id': oid, 'sale_client_order_ref': cor, 'sale_state': st }
        return result


    _columns = {
        'premerge_sale_id': fields.many2one('sale.order', 'Pre-Merge Sales Order Reference'),
        'sale_client_order_ref': fields.function(_get_sale_details, method=True, multi="details", type='char', size=64, string="Sale Client Order Ref"),
        'sale_state': fields.function(_get_sale_details, method=True, multi="details", type='char', size=32, string="Sale State"),
        'sale_lookup_order_id': fields.function(_get_sale_details, method=True, multi="details", type='many2one', relation="sale.order", size=32, string="Sale Order for Lookups"),
        'sale_lookup_type': fields.function(_get_sale_details, method=True, multi="details", type='char', size=32, string="Sale Order Lookup Type"),
    }
        
stock_move()
