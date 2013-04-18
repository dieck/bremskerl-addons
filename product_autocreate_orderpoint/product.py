# -*- coding: utf-8 -*-

from osv import osv, fields
from types import * 

class product(osv.osv):
    _name = "product.product"
    _inherit = _name

    def create(self, cr, uid, vals, context=None):
        c_id = super(product, self).create(cr, uid, vals, context)
        
        prd = self.browse(cr, uid, c_id)
        
        if (prd.type == 'product'):
            # find warehouse_id
            company_id = self.pool.get('res.company')._company_default_get(cr, uid, 'product.template', context=context)
            wh_obj = self.pool.get("stock.warehouse")
            whs = wh_obj.search(cr, uid, [('company_id','=',company_id)], context=context)
            if (whs):
                # found warehouse, so create orderpoint
                wh = wh_obj.browse(cr, uid, whs[0], context=context)        
                    
                msr_obj = self.pool.get("stock.warehouse.orderpoint")
                
                name = None
                if (prd.default_code):
                    name = "OP/" + prd.default_code
                else:
                    name = self.pool.get('ir.sequence').get(cr,uid,'stock.orderpoint') or ''
                      
                v = {   "name": name,
                        "warehouse_id": wh.id or 0,
                        "location_id": wh.lot_stock_id and wh.lot_stock_id.id or 0,
                        "product_uom": prd.uom_id and prd.uom_id.id or 0,
                        "product_id": c_id,
                        "product_min_qty": 0,
                        "product_max_qty": 0
                     }
                msr_obj.create(cr, uid, v, context=context)
        
        return c_id
        
    def write(self, cr, uid, ids, values, context=None):
        r = super(product, self).write(cr, uid, ids, values, context)
        
        wh_obj = self.pool.get("stock.warehouse")
        msr_obj = self.pool.get("stock.warehouse.orderpoint")

        company_id = self.pool.get('res.company')._company_default_get(cr, uid, 'product.template', context=context)
        whs = wh_obj.search(cr, uid, [('company_id','=',company_id)], context=context)
        if (not whs):
            # no warehouse found, so I won't be able to insert orderpoints anyway
            return r
        wh = wh_obj.browse(cr, uid, whs[0], context=context)        

        if ( (not (type(ids) is ListType)) and (not (type(ids) is TupleType)) ):
            ids = [ids] 

        for prd in self.browse(cr, uid, ids, context=context):
            if (prd.type == 'product'):
                # search for minimum stock rule
                    msr_ids = msr_obj.search(cr, uid, [('product_id','=',prd.id)], context=context)
                    if (not msr_ids):
                        # no rule found, so create one
                            
                        name = None
                        if (prd.default_code):
                            name = "OP/" + prd.default_code
                        else:
                            name = self.pool.get('ir.sequence').get(cr,uid,'stock.orderpoint') or ''
                      
                        msr_obj = self.pool.get("stock.warehouse.orderpoint")
                        v = {   "name": name,
                                "warehouse_id": wh.id or 0,
                                "location_id": wh.lot_stock_id and wh.lot_stock_id.id or 0,
                                "product_id": prd.id,
                                "product_uom": prd.uom_id and prd.uom_id.id or 0,
                                "product_min_qty": 0,
                                "product_max_qty": 0
                             }
                        msr_obj.create(cr, uid, v, context=context)

        return r
    
product()
