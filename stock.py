# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_move_price_history(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def _get_product_standard_price_currency(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            #TODO remove debug message
            print "GOT NEW CURRENCY FOR", session.id
            res[session.id] = session.product_id.product_tmpl_id.company_id.currency_id.id
        return res

    def _get_product_standard_price(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            #TODO remove debug message
            print "GOT NEW PRICE FOR", session.id
            res[session.id] = session.product_id.product_tmpl_id.standard_price
        return res
    
    def _is_to_be_updated(self, cr, uid, ids, context={}):
        res = []
        for session in self.browse(cr, uid, ids):
            if (session.state == 'done'):
                #TODO remove debug message
                print "STOCK MOVE TO BE UPDATED", session.id
                res.append(session.id)
        return res
    
    _columns = {
        'history_price_unit': fields.function(_get_product_standard_price, string="Historic Unit Price", type="float", method=True,
                                              store={'stock.move':(_is_to_be_updated,['state'],10)}), 
        'history_price_unit_currency_id': fields.function(_get_product_standard_price_currency, string="Historic Unit Price Currency",
                                                          type="many2one", relation="res.currency", method=True,
                                                          store={'stock.move':(_is_to_be_updated,['state'],20)}), 
    }
    
stock_move_price_history()
