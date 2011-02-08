
from osv import osv, fields

class product_wva_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'wva': fields.char("WVA number", size=10),
    }
            
product_wva_product()
