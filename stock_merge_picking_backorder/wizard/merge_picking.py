# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################

from osv import osv

class stock_picking_merge_wizard_backorder(osv.osv_memory):
    _name = "stock.picking.merge.wizard"
    _inherit = "stock.picking.merge.wizard" 
  
    # fieldname: function handling that fieldname
    # will not be raised as incompatibility error
    # def specialhandler(cr, uid, fieldname, merge, target, target_changes, context=None)
    # specialhandlers = { 'relation_fieldname': specialhandler, }
    
    def specialhandler_backorderid(self, cr, uid, fieldname, merge, target, target_changes, context=None):
        stock_move = self.pool.get('stock.move')
        
        # if it was merged before, we already have a premerge_backorder_id. We have to filter, if we want to overwrite
        # TODO: make a configuration wizard to choose this behaviour
        overwrite_at_second_merge = False
        
        # these are the moves that will be merged (where the picking will be deleted afterwards)
        line_ids = [line.id for line in merge.move_lines]
        # see if we want to overwrite, or if we want to keep. in that case, remove the existing lines from write list
        if (not overwrite_at_second_merge):
            line_ids = stock_move.search(cr, uid, [('id','in',line_ids),('premerge_backorder_id','=',False)])
        # store premerge_sale_id to all moves that are left        
        stock_move.write(cr, uid, line_ids, {'premerge_backorder_id': merge.backorder_id.id}, context=context)

        # these are the moves that will be merged INTO (where the picking will stay as target picking afterwards)
        line_ids = [line.id for line in target.move_lines]
        # see if we want to overwrite, or if we want to keep. in that case, remove the existing lines from write list
        if (not overwrite_at_second_merge):
            line_ids = stock_move.search(cr, uid, [('id','in',line_ids),('premerge_backorder_id','=',False)])
        # store premerge_sale_id to all moves that are left        
        stock_move.write(cr, uid, line_ids, {'premerge_backorder_id': target.backorder_id.id}, context=context)

        return target_changes
    
    specialhandlers = {
        'backorder_id': "specialhandler_backorderid"
    }

stock_picking_merge_wizard_backorder()
