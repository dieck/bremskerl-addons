# -*- coding: utf-8 -*-

from osv import osv, fields

class purchase_order_partnerref(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    _columns = {
        'partner_ref': fields.related("partner_id", "ref", type="char", string="Partner ref.", readonly=True),
    }
            
purchase_order_partnerref()
