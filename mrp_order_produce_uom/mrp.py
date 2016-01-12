# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_product_produce(osv.osv_memory):
    _name = "mrp.product.produce"
    _inherit = "mrp.product.produce"
    
    _columns = {
        'product_uom': fields.many2one("product.uom", string="UoM"),
    }
            
            
    def _get_product_uom(self, cr, uid, context=None):
        if context is None:
            context = {}
        prod = self.pool.get('mrp.production').browse(cr, uid,
                                context['active_id'], context=context)
        return prod.product_uom.id

    _defaults = {
         'product_uom': _get_product_uom,
    }

mrp_product_produce()
