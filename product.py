# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class product_uom_unique_uopm(osv.osv):
    _name = "product.uom"
    _inherit = "product.uom"
  
    _sql_constraints = [ ('default_code_uniq', 'unique (name, category_id)', """UoM name has to be unique per category."""), ]
        
product_uom_unique_uopm