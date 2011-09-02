# -*- coding: utf-8 -*-

from osv import fields, osv

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name

    def _has_module(self, cr, uid, name):
        module_pool = self.pool.get('ir.module.module')
        res = module_pool.search(cr, uid, [('name','=',name),('state','=','installed')])
        return (len(res)>0) # found anything => module is there and installed
        
    def _get_sale_details(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        
        for record in self.browse(cr, uid, ids, context=context):
            cor = None
            st = None
            oid = None
            solt = None

            # order to lookup:
            # sale_line_id exists => will not be changed by merges
            # picker_sale_id or premerge_sale_id exists => use stored information
            # use sale_id in picking
            
            if record.sale_line_id:
                if (record.sale_line_id.order_id):
                    solt = "Sale Line from Stock Move"
                    oid = record.sale_line_id.order_id.id
                    cor = record.sale_line_id.order_id.client_order_ref or False
                    st = record.sale_line_id.order_id.state or False

            if solt is None and self._has_module(cr, uid, "stock_merge_picking_sale"):
                if (record.premerge_sale_id):
                    solt = "Pre-Merge stored Sale Order"
                    oid = record.premerge_sale_id.id
                    cor = record.premerge_sale_id.client_order_ref or False
                    st = record.premerge_sale_id.state or False

            if solt is None and self._has_module(cr, uid, "stock_move_repick"):
                if (record.premerge_sale_id):
                    solt = "Pre-RePick stored Sale Order"
                    oid = record.premerge_sale_id.id
                    cor = record.premerge_sale_id.client_order_ref or False
                    st = record.premerge_sale_id.state or False

            if solt is None and self._has_module(cr, uid, "stock_picking_picker"):
                if (record.premerge_sale_id):
                    solt = "Pre-Merge stored Sale Order"
                    oid = record.premerge_sale_id.id
                    cor = record.premerge_sale_id.client_order_ref or False
                    st = record.premerge_sale_id.state or False
                
            if solt is None and record.picking_id:
                if (record.picking_id.sale_id):
                    solt = "Sale Order of Stock Picking"
                    oid = record.picking_id.sale_id.id
                    cor = record.picking_id.sale_id.client_order_ref or False
                    st = record.picking_id.sale_id.state or False
            
            result[record.id] = {'sale_lookup_type': solt, 'sale_lookup_order_id': oid, 'sale_client_order_ref': cor, 'sale_state': st }
        return result


    _columns = {
        'sale_client_order_ref': fields.function(_get_sale_details, method=True, multi="details", type='char', size=64, string="Sale Client Order Ref"),
        'sale_state': fields.function(_get_sale_details, method=True, multi="details", type='char', size=32, string="Sale State"),
        'sale_lookup_order_id': fields.function(_get_sale_details, method=True, multi="details", type='many2one', relation="sale.order", size=32, string="Sale Order for Lookups"),
        'sale_lookup_type': fields.function(_get_sale_details, method=True, multi="details", type='char', size=32, string="Sale Order Lookup Type"),
    }
        
stock_move()
