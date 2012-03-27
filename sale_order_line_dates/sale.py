# -*- coding: utf-8 -*-

from osv import osv, fields

from datetime import datetime
from dateutil.relativedelta import relativedelta

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _name = _inherit 
    
    def _get_effective_date(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = '2100-12-31' # for min() below
                
            for move in line.move_ids:
                d = move.picking_id and move.picking_id.date or '2100-12-31'
                res[line.id] = min(res[line.id], d)
         
            # remove dummy entries
            if (res[line.id] == '2100-12-31'):
                res[line.id] = None
                
        return res
    
    # analogue to sale_order_dates, Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
    def _get_commitment_date(self, cr, uid, ids, name, arg, context={}):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            dt = datetime.strptime(line.order_id.date_order, '%Y-%m-%d') + relativedelta(days=line.delay or 0.0)
            dt_s = dt.strftime('%Y-%m-%d')
            res[line.id] = dt_s
        return res

    _columns = {
        "commitment_date": fields.function(_get_commitment_date, type="date", string="Commitment Date", method=True, readonly=True, help="Estimated date from order date and delivery lead time."),
        "effective_date": fields.function(_get_effective_date, type="date", string="Effective Date", method=True, readonly=True, help="Date on which picking is created."),
        "requested_date": fields.related("order_id", "requested_date", type="date", string="Requested Date", help="Date on which customer has requested for sales."),
    }

sale_order_line()
