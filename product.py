
from osv import osv, fields

class product_wva_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'wva': fields.integer("WVA number"),
    }
            
product_wva_product()
