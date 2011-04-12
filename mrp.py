# -*- coding: utf-8 -*-

from osv import osv, fields
import decimal_precision as dp

class mrp_bom(osv.osv):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    
    _columns = {
        'product_uos_qty': fields.float('Product UOS Qty', digits_compute=dp.get_precision('Bill of Material Quantities')),
        'product_qty': fields.float('Product Qty', required=True, digits_compute=dp.get_precision('Bill of Material Quantities')),
        'product_rounding': fields.float('Product Rounding', help="Rounding applied on the product quantity.", digits_compute=dp.get_precision('Bill of Material Quantities')),
    }
    
mrp_bom()
    
