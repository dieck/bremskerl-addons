# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class product_code_unique_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
  
    _sql_constraints = [ ('default_code_uniq', 'unique (default_code)', """Reference has to be unique."""), ]

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}

        product = self.read(cr, uid, id, ['default_code'], context=context)
        if not default:
            default = {}
        default = default.copy()
        default['default_code'] = product['default_code'] + _(' (copy)')

        return super(product_code_unique_product, self).copy(cr=cr, uid=uid, id=id, default=default, context=context)
        
product_code_unique_product()
