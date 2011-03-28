# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_move_price_history(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def _get_product_standard_price_currency(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            res[session.id] = session.product_id.product_tmpl_id.company_id.currency_id.id
        return res

    def _get_product_standard_price(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            res[session.id] = session.product_id.product_tmpl_id.standard_price
        return res
    
    def _get_changed_product_ids(self, cr, uid, ids, context={}):
        return ids
    
    
    _columns = {
        'history_price_unit': fields.function(_get_product_standard_price, string="Historic Unit Price", type="float", method=True,
                                              store={'stock.move':(_get_changed_product_ids,['product_id'],10)}), 
        'history_price_unit_currency_id': fields.function(_get_product_standard_price_currency, string="Historic Unit Price Currency",
                                                          type="many2one", relation="res.currency", method=True,
                                                          store={'stock.move':(_get_changed_product_ids,['product_id'],10)}), 
    }
    
stock_move_price_history()
