# -*- coding: utf-8 -*-
from osv import osv, fields

class product_product(osv.osv):
    _name = "product.product"
    _inherit = _name
    
    def _get_supplier_productcode(self, cr, uid, ids, fields, arg, context=None):
        result = {}
        for p in self.browse(cr, uid, ids, context=context):
            suppcode = p.seller_ids and p.seller_ids[0] and p.seller_ids[0].product_code or None
            result[p.id] = suppcode 
        return result
    
    _columns = {
        'supplier_product_code': fields.function(_get_supplier_productcode, method=True, store=True, type='char', size=64, string='Supplier Product Code', 
                                help="For more than one supplier, this is a NON-DETERMINISTIC suppliers product code (though most likely from the first supplier configured)."),
    }
            
product_product()
