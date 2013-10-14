# -*- coding: utf-8 -*-
from osv import fields, osv
import time

class stock_move_date_expected_log(osv.osv):
    _name = "stock.move.dateexpectedlog"
        
    _columns = {
        'changed_date': fields.datetime('Changed on', readonly=False),
        'changed_uid': fields.many2one('res.users', 'Changed by', readonly=False),
        'move_id': fields.many2one("stock.move", "Stock Move", required=True),
        'prev_date_expected': fields.datetime('Previously Scheduled Date', required=False), # false for initial
        'new_date_expected': fields.datetime('New Scheduled Date', required=True),
        'picking_id': fields.related('move_id', 'picking_id', type='many2one', relation="stock.picking", string="Picking"),
        'partner_id': fields.related('move_id', 'partner_id', type='many2one', relation="res.partner", string="Partner"),
    }
    
    _defaults = {
        "changed_date": lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        "changed_uid": lambda self,cr,uid,context: uid,
    }

stock_move_date_expected_log()    

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def write(self, cr, uid, ids, vals, context=None):
        # object for writing log files
        smdel_obj = self.pool.get('stock.move.dateexpectedlog')

        # only write log if date_expected is to be changed anyway        
        if vals.get('date_expected', False):
            # fetch previous record
            for prev in self.browse(cr, uid, ids):
                # if date_expected changed
                if (prev.date_expected != vals['date_expected']):
                    # create log entry
                    log = {'move_id': prev.id, 'prev_date_expected': prev.date_expected, 'new_date_expected': vals['date_expected']}
                    smdel_obj.create(cr, uid, log, context=context)
        
        return super(stock_move, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        new_id = super(stock_move, self).create(cr, uid, vals, context=context) 

        # create "initial" log entry, if new date_expected exists
        if vals.get('date_expected', False):
            smdel_obj = self.pool.get('stock.move.dateexpectedlog')
            log = {'move_id': new_id, 'prev_date_expected': None, 'new_date_expected': vals['date_expected']}
            smdel_obj.create(cr, uid, log, context=context)

        return new_id 
    

stock_move()
