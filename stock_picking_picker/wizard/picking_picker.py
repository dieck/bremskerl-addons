# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################

from osv import osv, fields

class stock_picking_picker_wizard(osv.osv_memory):
    _name = "stock.picking.picker.wizard"
    _description = "Pick Stock Pickings"
    
    def do_create_picking(self, cr, uid, ids, context=None):
        print "ctx", context
        
        

stock_picking_picker_wizard()

