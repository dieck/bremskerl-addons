# -*- coding: utf-8 -*-

from osv import fields, osv

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def get_mrp_bom_raw_materials_location_id(self, cr, uid, product_id):
        print "get_mrp_bom_raw_materials_location_id for product",product_id
        bom_pool = self.pool.get("mrp.bom")
        ids = bom_pool.search(cr, uid, [("product_id","=",product_id),("bom_id","=",False)])
        print "get_mrp_bom_raw_materials_location_id ids",ids
        res = bom_pool.read(cr, uid, ids, ['raw_materials_location_id'])
        print "get_mrp_bom_raw_materials_location_id ids",res
        if len(res):
            if (len(res)>0):
                res0 = res[0]
                print "get_mrp_bom_raw_materials_location_id res0",res0
                if (res0):
                    res0rml = res0['raw_materials_location_id']
                    print "get_mrp_bom_raw_materials_location_id res0rml",res0rml
                    if (res0rml):
                        res0rml0 = res0rml[0]
                        print "get_mrp_bom_raw_materials_location_id res0rml0",res0rml0
                        if (res0rml0):
                            return res0rml0
        return 0
        

    def debug_warehouse(self, cr, uid, id):
        warehouse_pool = self.pool.get("stock.warehouse")
        for warehouse in warehouse_pool.browse(cr, uid, [id]):
            print "WH ", id, warehouse.id, warehouse.name, warehouse.lot_stock_id.id, warehouse.lot_stock_id.name
        

    def action_ship_create(self, cr, uid, ids, *args):
        # one of the dirtiest workarounds I ever made
        # looking which stocks are used
        # storing them, and overwrite them with BoM Raw Materials Location, if defined
        # calling super() to process
        # writing back the old lot_stock_ids
               
        storage = {}       
                
        warehouse_pool = self.pool.get("stock.warehouse")
                
        for order in self.browse(cr, uid, ids, context={}):
            for line in order.order_line:
                if line.state == 'done':
                    continue
                if line.product_id and line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    bom_rml_id = self.get_mrp_bom_raw_materials_location_id(cr, uid, line.product_id.id)
                    if (bom_rml_id > 0):
                        print "got get_mrp_bom_raw_materials_location_id",bom_rml_id
                        self.debug_warehouse(cr, uid, order.shop_id.warehouse_id.id)
                        storage[line.id] = {"warehouse_id": order.shop_id.warehouse_id.id, 
                                            "original_id": order.shop_id.warehouse_id.lot_stock_id.id,
                                            "bom_rml_id": bom_rml_id,
                                            }
                    else:
                        print "got NO get_mrp_bom_raw_materials_location_id"

        print "have storage",storage

        for st_id in storage:
            st = storage[st_id]
            print "found storage",st
            if (st["bom_rml_id"] > 0):
                print "updateing warehouse", st["warehouse_id"], "with location", st["bom_rml_id"], "instead of", st["original_id"]
                warehouse_pool.write(cr, uid, [st["warehouse_id"]], {'lot_stock_id': st["bom_rml_id"]})
                self.debug_warehouse(cr, uid, st["warehouse_id"])

        ret = super(sale_order, self).action_ship_create(cr=cr, uid=uid, ids=ids)
        
        for st_id in storage:
            st = storage[st_id]
            if (st["bom_rml_id"] > 0):
                print "rollback warehouse", st["warehouse_id"], "from location", st["bom_rml_id"], "to", st["original_id"]
                self.debug_warehouse(cr, uid, st["warehouse_id"])
                warehouse_pool.write(cr, uid, [st["warehouse_id"]], {'lot_stock_id': st["original_id"]})
                self.debug_warehouse(cr, uid, st["warehouse_id"])

        return ret
    
sale_order()