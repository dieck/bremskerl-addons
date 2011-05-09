# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

import time


class boilerplates_category(osv.osv):
    _name = "boilerplates.category"
    _columns = {
        "name": fields.char("Name", size=64, required=True, translate=True),
        "description": fields.text("Description"),
    }
    _sql_constraints = [
        ('boilerplates_category_name_unique', 'unique (name)', _('The boilerplate category names must be unique!')),
    ]
boilerplates_category()
      

class boilerplates_text(osv.osv):
    _name = "boilerplates.text"

    def _is_active(self, cr, uid, ids, field_name, arg, context):
        res = {}
        now = time.strftime('%Y-%m-%d') #TODO is there a better way? Looks somehow wrong using a "string" for comparing dates
        for session in self.browse(cr, uid, ids):
            if (not session.valid_to):
                res[session.id] = (session.valid_from <= now)
            else:
                res[session.id] = ((session.valid_from <= now) and (session.valid_to >= now)) 
        return res
    
    _columns = {
        "name": fields.char("Name", size=64, required=True, translate=True),
        "category_id": fields.many2one("boilerplates.category", "Category", required=True),
        
        "valid_from": fields.date("Valid From", required=True),
        "valid_to": fields.date("Valid To"),

        "product_id": fields.many2one("product.product", "Product", help="This note relates to this single specific product."),
        "partner_id": fields.many2one("res.partner", "Partner", help="This note relates to this single specific partner."),

        "text": fields.text("Text", translate=True),
        "note": fields.text("Internal notes about this boilerplate", translate=True),
                        
        "active": fields.function(_is_active, string="Valid", type='boolean', method=True),
    }
    _sql_constraints = [
        ('boilerplates_text_name_unique', 'unique (name)', _('The boilerplate names must be unique!')), #TODO company
    ]
    _constraints = [
        #TODO constraint: boilerplate names must be unique per time frame (#TODO2 per company)
    ]
    _defaults = {
        "valid_from": lambda *a: time.strftime('%Y-%m-%d'),
       #TODO company "company_id": lambda self, cr, uid, *a: self.pool.get('res.users').browse(cr,uid,uid).company_id.id,
    }
boilerplates_text()
