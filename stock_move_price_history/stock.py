# -*- coding: utf-8 -*-
from osv import fields, osv
import decimal_precision as dp
import time

class stock_move_price_history(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    
    # TODO Oh my god, what did I do here... Sorry to all who have to see this :) Please rewrite me...  md 2013-03-14
    # Would work much more simplier, and easier to read and understand:
    # superseed .write and .create to look for a change to state=done, then set the history_price_unit and currency.
    
    # do updates. works as an update determination function
    def _smph_do_updates(self, cr, uid, ids, context={}):
        res = []
        for session in self.browse(cr, uid, ids):
            # if state is set to done
            if (session.state == 'done'):
                # and there is not yet stored a price
                if (not (session.history_price_unit)):
                    # store price and unit (id)
                    self.write(cr, uid, [session.id], {
                        'history_price_unit': session.product_id.product_tmpl_id.standard_price,
                        'history_price_unit_currency_id_store': session.product_id.product_tmpl_id.company_id.currency_id.id})
                    
                # return list of ids to be updated with _smph_get_current_date
                res.append(session.id)
        return res


    # returns current date for all ids
    def _smph_get_current_date(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for id in ids:
            res[id] = time.strftime('%Y-%m-%d %H:%M:%S'),
        return res

    # "converts" a integer field to many2one via fields.function
    def _smph_get_currency_from_id(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            # use the stored id as real many2one id
            res[session.id] = session.history_price_unit_currency_id_store
        return res
    
    _columns = {
         # store price
         'history_price_unit' : fields.float('Historic Unit Price', digits_compute=dp.get_precision('Purchase Price')),

         # store only id, not relation
         'history_price_unit_currency_id_store': fields.integer('Internal storage for Historic Unit Price Currency'),
         
         # get relation from id
         'history_price_unit_currency_id': fields.function(_smph_get_currency_from_id, string="Historic Unit Price Currency", type="many2one", relation="res.currency", method=True),
         
         # use this as a dummy trigger function to set the values, from _smph_do_updates
         'history_price_dummytrigger': fields.function(_smph_get_current_date, string="Dummy Trigger: Last Update", type="datetime", method=True,
                                              store={'stock.move':(_smph_do_updates,['state'],20)}), 
    }
    
stock_move_price_history()
