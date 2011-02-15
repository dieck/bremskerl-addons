# -*- coding: utf-8 -*-

from osv import osv, fields

class product_qa_documentation_type_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'qa_doctype': fields.char("Type of documentation", size=50),
    }
            
product_qa_documentation_type_product()
