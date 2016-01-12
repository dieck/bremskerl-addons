# -*- coding: utf-8 -*-

from osv import osv, fields

class product_origin_country(osv.osv):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'origin_country_id': fields.many2one("res.country", "Country of Origin", help="Made in ..."),
    }
            
product_origin_country()
