# -*- coding: utf-8 -*-
from osv import fields, osv

class stock_move_price_history(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def _get_product_standard_price_currency(self, cr, uid, ids, field_name, arg, context):
        print "CURRENCY1"
        res = {}
        for session in self.browse(cr, uid, ids):
            #TODO remove debug message
            print "GOT NEW CURRENCY FOR", session.id
            res[session.id] = session.product_id.product_tmpl_id.company_id.currency_id.id
        print "CURRENCY2"
        return res

    def _get_product_standard_price(self, cr, uid, ids, field_name, arg, context):
        res = {}
        print "PRICE1"
        for session in self.browse(cr, uid, ids):
            #TODO remove debug message
            print "GOT NEW PRICE FOR", session.id
            res[session.id] = session.product_id.product_tmpl_id.standard_price
        print "PRICE2"
        return res
    
    def _is_to_be_updated(self, cr, uid, ids, context={}):
        ## can be replaced by
        # return self.search(cursor, user_id, [('id','in',ids),('state', '=', 'done')])
        res = []
        print "IS1"
        for session in self.browse(cr, uid, ids):
            if (session.state == 'done'):
                #TODO remove debug message
                print "STOCK MOVE TO BE UPDATED", session.id
                res.append(session.id)
        print "IS2"
        return res
    
    _columns = {
        'history_price_unit': fields.function(_get_product_standard_price, string="Historic Unit Price", type="float", method=True,
                                              store={'stock.move':(_is_to_be_updated,['state'],20)}), 
        'history_price_unit_currency_id': fields.function(_get_product_standard_price_currency, string="Historic Unit Price Currency",
                                                          type="many2one", relation="res.currency", method=True,
                                                          store={'stock.move':(_is_to_be_updated,['state'],10)}), 
    }
    
stock_move_price_history()
