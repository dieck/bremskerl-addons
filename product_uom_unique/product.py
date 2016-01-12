# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class product_uom_unique_uom(osv.osv):
    _name = "product.uom"
    _inherit = "product.uom"
  
    _sql_constraints = [ ('product_uom_name_uniq', 'unique (name, category_id)', """UoM name has to be unique per category."""), ]
        
product_uom_unique_uom
