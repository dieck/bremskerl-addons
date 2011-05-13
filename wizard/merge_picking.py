# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
#
#    Merge Picking up to v5 of OpenERP was written by Axelor, www.axelor.com
#    This is a complete rewrite.
#
##############################################################################

from osv import osv

class stock_picking_merge_wizard_sale(osv.osv_memory):
    _name = "stock.picking.merge.wizard"
    _inherit = "stock.picking.merge.wizard" 
  
    # fieldname: function handling that fieldname
    # will not be raised as incompatibility error
    # def specialhandler(cr, uid, fieldname, merge, target, target_changes, context=None)
    # specialhandlers = { 'relation_fieldname': specialhandler, }
    
    def specialhandler_saleid(self, cr, uid, fieldname, merge, target, target_changes, context=None):
        debug = True
        
        if debug:
            print "starting specialhandler saleid for fn,mr,tg", fieldname, merge, target
            print "mlines", merge.move_lines
        
            # copy sale_id into stock moves
            for ml in merge.move_lines:
                print "ml",ml
                print "mlid",ml.id
        
        line_ids = [line.id for line in merge.move_lines]
        self.pool.get('stock.move').write(cr, uid, line_ids, {'premerge_sale_id': merge.sale_id.id}, context=context)
        
        if debug:
            print "  updated line_ids",line_ids,"with premerge_sale_id",merge.sale_id.id
        

        line_ids = [line.id for line in target.move_lines]
        self.pool.get('stock.move').write(cr, uid, line_ids, {'premerge_sale_id': target.sale_id.id}, context=context)

        return target_changes
    
    specialhandlers = {
        'sale_id': "specialhandler_saleid"
    }

stock_picking_merge_wizard_sale()
