
from osv import osv, fields

class product_code_mandatory_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
        
    _columns = {
        'code': fields.function(lambda self, *args, **kwargs: self._product_code(*args, **kwargs),
                                method=True, type='char', string='Reference blah', required=True),
    }
            
product_code_mandatory_product()
